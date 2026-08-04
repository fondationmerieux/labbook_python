# 08 — OAuth2 et sécurité de l'API

## 8.1 Ce que ça remplace

À mesure que LabBook a exposé davantage de services REST, la question s'est posée de savoir
comment garantir que seuls un utilisateur ou une application autorisés puissent les appeler.

Le mécanisme précédent était une **authentification basique** : identifiant et mot de passe
transmis à chaque appel, en clair ou presque.

LabBook suit désormais **OAuth 2.0**. Le principe : plutôt que de transmettre un mot de
passe à chaque requête, l'application obtient un **jeton d'accès** (*token*), qu'elle
présente ensuite dans l'en-tête de chacun de ses appels.

L'implémentation s'appuie sur **Authlib** (`labbook_BE/app/security/oauth_routes.py`).

## 8.2 Deux types de clients

| Type | Qui | Flux |
|---|---|---|
| `authorization_code` | le front end LabBook | code d'autorisation, avec PKCE |
| `client_credentials` | un logiciel tiers | authentification directe de machine à machine |

Dans les deux cas, le jeton vit **2 heures** (`labbook_BE/app/__init__.py:123-125`), en dur.

Pour le front end, le renouvellement est transparent : il se fait au fil de la navigation.
Un logiciel tiers, lui, doit redemander un jeton toutes les deux heures — c'est délibéré :
la porte ne reste pas ouverte indéfiniment.

## 8.3 Les trois tables

| Table | Contenu | Remarque |
|---|---|---|
| `oauth2_client` | les applications autorisées : identifiant, secret, URLs de redirection, portées, actif ou non | |
| `oauth2_code` | les codes d'autorisation temporaires | **toujours vide, ou presque** : un code est supprimé dès qu'il est utilisé |
| `oauth2_token` | les jetons émis : chaîne, durée de vie, portées, état révoqué | conservée, elle grossit avec le temps |

Ces tables suivent la norme OAuth2. Certaines colonnes ne sont pas utilisées aujourd'hui :
le schéma respecte la norme pour rester ouvert.

## 8.4 Le mécanisme, pas à pas

Le front end et le back end partagent un secret, `oauth_client_secret.py`, écrit dans
`/storage/key/` par le `gunicorn.sh` du front end à la première installation (chapitre
[00](00-architecture.md)). C'est ce secret commun qui leur permet de se reconnaître.

```
1. L'utilisateur ouvre une page. Pas de jeton en session.
2. Le front end demande un CODE au back end (ils partagent le secret).
   → le code est valable 1 minute, à usage unique, stocké dans oauth2_code
3. Le front end présente immédiatement ce code et demande un JETON.
   → le jeton est valable 2 heures, stocké dans oauth2_token
4. Chaque appel à /services/... transporte ce jeton dans son en-tête.
5. Jeton absent, expiré ou révoqué → 401 Unauthorized
```

L'échange se fait donc en **deux temps** — un code court, puis un jeton — plutôt qu'en
délivrant directement un jeton.

> **Note.** Le secret est engendré une fois par installation et n'est jamais régénéré, même
> après reconstruction du conteneur, puisqu'il vit dans le volume de stockage. Supprimer le
> fichier en force un nouveau au démarrage suivant — et invalide tout ce qui existait.

## 8.5 Protéger, ou non, un service

Le décorateur, dans `services/*Rest.py` :

```python
class DoctorList(Resource):
    @require_oauth()
    def post(self):
        ...
```

Le retirer rend le service accessible sans jeton. C'est le cas de huit endpoints, repérés
par le commentaire `# no oauth required` dans `app/__init__.py` :

- vérifications d'initialisation et de version ;
- interrogation de l'état d'une restauration en cours ;
- points d'entrée utilisés par les automates via LabBook Connect (`AnalyzerLab27`,
  `AnalyzerLab29`, …).

Ces derniers ne sont pas protégés parce que **LabBook Connect ne gère pas encore OAuth2** :
l'intégration a été demandée pour LabBook seul. Le jour où Connect saura présenter un jeton,
ces exemptions disparaîtront et une ligne cliente lui sera créée dans `oauth2_client`.

## 8.6 Portées

Un client se voit attribuer une liste de portées (*scopes*), qui limitent les services
qu'il peut atteindre. Le client `labbook-api`, celui de la page Swagger, est par exemple
restreint aux portées `external_analysis`, `external_patient`, `external_record`,
`external_result`, `external_user`.

Portées et CORS sont deux protections distinctes et complémentaires : le CORS limite les
**origines** autorisées à `/services/external/*` (chapitre [07](07-back-end.md)), les portées
limitent les **services** qu'un client donné peut appeler.

## 8.7 Déclarer un client

Deux clients existent sur une base neuve :

| Client | Rôle |
|---|---|
| `labbook-FE` | le front end. Non supprimable depuis l'interface. |
| `labbook-api` | la page Swagger `/sigl/api`. |

Pour un logiciel tiers, passez par l'interface : **Configuration → Clients OAuth**, plus
sûre qu'une insertion en base. Vous y définissez identifiant, secret, URLs de redirection et
portées.

La case **actif** permet de couper l'accès d'un client sans supprimer sa configuration —
pratique pour suspendre un prestataire et le rétablir ensuite.

> **Piège — supprimer `labbook-api`.** L'interface permet de le supprimer. La page Swagger
> cesse alors de fonctionner, et il faut le recréer **à l'identique** : elle recherche ce
> client par son identifiant exact.

## 8.8 Intégrer un logiciel tiers

OAuth2 se déboguant mal en aveugle, procédez par étapes :

1. **Retirer temporairement `@require_oauth()`** du service visé, reconstruire, et vérifier
   que le logiciel tiers atteint bien l'API et obtient les données attendues. Vous validez
   ainsi l'URL, le format et le réseau, sans mêler l'authentification.
2. **Remettre le décorateur**, déclarer le client dans `oauth2_client` avec les bonnes
   portées, et faire fonctionner l'authentification.

Traiter les deux problèmes séparément fait gagner beaucoup de temps.

Rien n'oblige à ce que le service visé soit sous `/services/external/` : il suffit que la
portée le permette. Mais si vous exposez un service interne, la pratique du projet est d'en
publier un doublon sous `/services/external/`, pour que la liste de ce qui est exposé reste
lisible.

## 8.9 La page Swagger

`/sigl/api` sert une interface **Swagger / OpenAPI**, décrite par
`labbook_FE/app/templates/app-swagger-api.yaml`. Elle documente une dizaine de services
externes et permet de les essayer depuis le navigateur, sans écrire de `curl`.

Il faut s'y autoriser avant de pouvoir lancer un appel : la page est elle-même soumise à
OAuth2, via le client `labbook-api`.

## 8.10 Traiter les erreurs OAuth à part

Convention du front end : une erreur d'authentification est traitée par une fonction
dédiée, distincte du traitement des autres erreurs.

La raison est pratique. Un appel peut échouer pour quantité de motifs ; savoir d'emblée si
le back end a **refusé faute d'authentification valide** ou s'il s'agit d'autre chose oriente
immédiatement le diagnostic. Un `401` renvoie vers le jeton et le client ; tout le reste
renvoie vers le code.
