# 07 — Développer côté back end

Le back end expose une API REST et c'est le **seul** composant qui parle à la base de
données. C'est là que se concentre le travail quotidien du développeur, et là qu'on casse le
plus de choses : une erreur dans un template dégrade une page, une erreur ici peut affecter
toute l'application.

## 7.1 Organisation

```
labbook_BE/
├── Pipfile
├── gunicorn.sh
├── alembic/                 chapitre 06
├── script/                  chapitre 09
└── app/
    ├── __init__.py          configuration + 290 déclarations de routes REST
    ├── services/*Rest.py    une classe par ressource : reçoit, valide, trace
    ├── models/*.py          le SQL et la logique métier
    ├── security/            OAuth2 (chapitre 08)
    ├── automation/          tâches planifiées (chapitre 09)
    ├── exception/           DBException, GenericException
    └── translations/        chapitre 05
```

Il n'y a **pas d'ORM**. Tout le SQL est écrit à la main.

### Le Pipfile du back end

Nettement plus fourni que celui du front end : `flask`, `flask-restful`, `authlib`,
`flask-cors`, `mysql-connector-python`, `alembic`, `sqlalchemy`, `relatorio`, `pdfkit`,
`reportlab`, `pikepdf`, `qrcode`, `python-barcode`, `babel`, `pip-audit`.

> **Note — `mysql-connector-python` est gelé.** Ce paquet ne peut pas être monté de version,
> et `pip-audit` signale d'ailleurs une vulnérabilité connue sur celui utilisé. La raison
> tient au parc installé : lors d'une mise à jour, Alembic s'exécute **avant** toute autre
> chose, et il a besoin de ce pilote. Une installation très ancienne tourne sur un MySQL 5.x
> qu'un pilote récent ne sait plus interroger. Monter la version rendrait ces sites
> incapables de se mettre à jour.

## 7.2 `app/__init__.py`

545 lignes, bien plus court que son équivalent front end : il configure, puis enregistre des
routes.

### Configuration

Imports, langues, préparation des deux logs (`log_services`, `log_db`), création de
l'application Flask, chargement de `default_settings.py` puis de `LOCAL_SETTINGS`, puis des
variables d'environnement — qui l'emportent.

Le back end reçoit en plus des chemins dont les scripts auront besoin : `LABBOOK_KEY_DIR`,
`LABBOOK_STATUS_DIR`, `LABBOOK_LOG_DIR`.

### CORS

```python
CORS(app, resources={r"/services/external/*": {...}})
```

Seuls les endpoints sous `/services/external/` sont ouverts à une origine externe. Tous les
autres ne sont atteignables que localement.

C'est une **convention**, pas une garantie : rien n'empêche techniquement d'appeler un autre
service avec la bonne portée OAuth. Mais garder les points d'entrée externes sous un préfixe
identifiable permet de savoir, d'un coup d'œil, ce qui est exposé. Si un logiciel tiers a
besoin d'un service qui n'existe qu'en interne, la pratique est d'en publier un doublon sous
`/services/external/`.

### OAuth2

```python
app.config['OAUTH2_TOKEN_EXPIRES_IN'] = {
    'client_credentials': 7200,   # 2 h — machine à machine
    'authorization_code': 7200,   # 2 h — front end LabBook
}
```

Deux heures, en dur. Voir le chapitre [08](08-oauth2.md).

### Audit trail

Chaque appel à l'API peut être tracé en base : qui, quand, quelle action, quel service,
quelles données. Fonctionnalité récente, et coûteuse.

> **Piège — l'audit sur disque lent.** Sur un serveur à disque mécanique 5400 tours partagé
> par plusieurs postes, l'audit ajoute un `INSERT` par action. Les insertions
> s'accumulent, la table se verrouille, et les utilisateurs constatent des attentes de dix à
> vingt secondes.
>
> Deux réponses : une case dans les préférences permet de **désactiver l'audit**, et la
> configuration MySQL livrée par l'ISO regroupe les écritures sur une seconde au lieu de les
> exécuter une par une. Ce regroupement fait respirer le disque, au prix de la perte d'au
> plus une seconde d'écritures en cas de coupure.

### Enregistrement des routes

```python
api.add_resource(DoctorList, '/services/doctor/list')
api.add_resource(AnalyzerLab27,
                 '/services/external/device/analyzer/lab27/<string:id_analyzer>')  # no oauth required
```

290 déclarations, une par ressource, classées par ordre alphabétique. **C'est la référence
unique de la surface d'URL du back end** : c'est ici qu'on commence quand on cherche d'où
part un service.

Les arguments d'URL doivent être typés : `<string:...>`, `<int:...>`. Une même ressource
peut porter plusieurs URLs.

Le commentaire `# no oauth required` marque les huit endpoints exemptés
d'authentification : vérifications d'initialisation et de version, interrogation de l'état
d'une restauration, points d'entrée utilisés par les automates via LabBook Connect — qui ne
gère pas encore OAuth2.

## 7.3 La chaîne complète

L'exemple type : afficher la liste des prescripteurs.

```
Front end : route  /doctor_list
   ↓  requests.post('/services/doctor/list', headers={jeton})
__init__.py        api.add_resource(DoctorList, '/services/doctor/list')
   ↓
services/DoctorRest.py     class DoctorList.post()
   ↓  Doctor.getDoctorList(...)
models/Doctor.py           construit et exécute le SQL
   ↓
MySQL
   ↓  remonte en JSON
Front end : render_template('list-doctor.html', ...)
```

Deux règles structurent tout le back end :

- **`services/` ne fait jamais de SQL.** Il valide les arguments, appelle un ou plusieurs
  modèles, met en forme la réponse, trace.
- **`models/` ne fait jamais d'audit.** L'audit décrit une intention (« supprimer un
  prescripteur »), pas un accès aux données. Il appartient donc à la couche du dessus.

## 7.4 La couche `services`

Un fichier par domaine, miroir de `models/` : `DoctorRest.py`, `PatientRest.py`,
`RecordRest.py`, `SettingRest.py`…

`GeneralRest.py` est le fourre-tout historique — traitements de dates, mise en forme des
réponses. Il subsiste quelques fonctions de dictionnaire qui auraient leur place dans
`DictRest.py`.

### Une classe par couple ressource/verbe

Trois verbes sont utilisés : `get`, `post`, `delete`. Une classe ne peut pas porter deux
`post`. Il faut donc **une classe par action** :

| Classe | Rôle |
|---|---|
| `DoctorList` | `post` — liste filtrée |
| `DoctorDet` | `get` — un prescripteur ; `post` — création ou mise à jour |
| `DoctorSearch` | `post` — recherche |
| `DoctorExport` | `post` — export CSV |

`post` est utilisé pour les listes parce que les critères de filtrage voyagent dans le corps
de la requête.

### Structure type

```python
class DoctorList(Resource):
    @require_oauth()                                   # 1. authentification
    def post(self):
        log = logging.getLogger('log_services')        # 2. log de la couche service

        args = request.get_json()
        if 'id_doctor' not in args:                    # 3. valider les arguments
            Audit.insert(..., 'missing arguments')
            return compose_ret('', Constants.cst_content_type['JSON'], 400)

        data = Doctor.getDoctorList(args)              # 4. appeler le modèle

        Audit.insert(..., 'success')                   # 5. tracer
        return compose_ret(data, Constants.cst_content_type['JSON'])
```

- **`@require_oauth()`** conditionne l'authentification. Le retirer rend le service
  accessible sans jeton — c'est ce qui distingue les huit endpoints exemptés.
- **`compose_ret`** (dans `models/General.py`) met en forme la réponse et positionne les
  en-têtes. Sans code explicite, c'est un `200`. On passe `400` pour une requête invalide,
  `500` pour une erreur interne. Elle sait aussi produire du HL7, utilisé par les services
  destinés aux automates.
- **Une distinction utile** : `id > 0` signifie mise à jour, `id == 0` signifie création. On
  la retrouve partout.

### Réutiliser plutôt que dupliquer

`DoctorExport` n'a pas son propre SQL : il appelle `getDoctorList`, le même modèle que
`DoctorList`, et se contente d'écrire le résultat dans un CSV. Le modèle reste mutualisé, la
mise en forme est spécifique.

## 7.5 La couche `models`

Un fichier par domaine : `Analysis`, `Patient`, `Record`, `Result`, `Product`, `Quality`,
`Report`, `Pdf`, `Setting`, `User`, `Automation`, `Audit`, `Dict`, `Export`, `File`, `Lite`…

`Various.py` et `Constants.py` portent les helpers et constantes transversales
(`Constants.cst_*` pour les chemins sous `/storage`, les codes d'état, les constantes HL7).

### `DB.py`

Le seul endroit où une connexion MySQL est ouverte. Il maintient une connexion de classe
unique, avec `ping(reconnect=True)` avant réutilisation — une machine mise en veille peut
avoir perdu la socket sans que rien ne le signale. `autocommit` est activé.

Les curseurs sont ouverts en mode dictionnaire : les résultats sont des dictionnaires
indexés par nom de colonne.

### Paramètres de requête

Deux syntaxes, imposées par le pilote MySQL :

**Positionnelle** — pour une requête à un ou deux paramètres :

```python
sql = "DELETE FROM sigl_08_data WHERE id_data = %s"
cursor.execute(sql, (id_item,))
```

L'ordre compte. Au-delà de deux ou trois paramètres, c'est illisible.

**Nommée** — pour tout le reste, en particulier `INSERT` et `UPDATE` :

```python
sql = "UPDATE sigl_08_data SET code = %(code)s, doc_agreement = %(doc_agreement)s WHERE ..."
cursor.execute(sql, args)
```

L'ordre devient indifférent.

> **Piège — le `s` oublié.** `%(code)` au lieu de `%(code)s` : Python ne dit rien. Pour lui
> ce n'est qu'une chaîne, évaluée seulement à l'exécution de la requête. Vous pouvez
> enregistrer, reconstruire, relancer — l'erreur ne se manifestera que le jour où quelqu'un
> utilise la fonction. Deuxième variante : le nom du paramètre dans la requête ne correspond
> pas à celui de la clé fournie. Même silence.
>
> Ces deux fautes sont les erreurs les plus fréquentes du projet. **Testez toute requête
> modifiée avant de livrer.**

### `fetchone` ou `fetchall`

- `fetchone()` quand la requête ne peut renvoyer qu'une ligne → un dictionnaire ;
- `fetchall()` sinon → une liste de dictionnaires.

Se tromper fait planter le code appelant, qui n'attend pas la même forme.

### Autres conventions

- un `INSERT` renvoie l'identifiant créé, ou `0` en cas d'échec ;
- les jointures portent une `LIMIT`, pour qu'une requête mal écrite ne fasse pas exploser la
  charge sur une grosse base ;
- le nettoyage des valeurs `None` en chaîne vide est fréquent avant renvoi, Flask s'en
  accommodant mal ;
- les libellés à traduire passent par le décorateur `_()`, comme côté front end, après appel
  de `Various.use_lang_db()` qui détermine la langue courante (chapitre
  [05](05-traductions.md)).

## 7.6 Le schéma de base

119 tables, décrites dans `doc/tables.md` avec une catégorie et une ligne d'explication.
Fichier maintenu à la main : pensez à l'alimenter en ajoutant une table.

### Deux générations de nommage

**Les tables historiques**, antérieures à la réécriture : `sigl_01_data` à `sigl_NN_data`.
Le nom ne dit rien de leur contenu, et leur clé primaire s'appelle systématiquement
`id_data`.

| Table | Contenu |
|---|---|
| `sigl_02_data` | dossiers |
| `sigl_03_data` | patients |
| `sigl_05_data` | analyses |
| `sigl_07_data` | variables |
| `sigl_08_data` | prescripteurs |

`doc/tables.md` existe précisément pour faire la correspondance.

**Les tables récentes** portent un nom parlant et un préfixe de trois ou quatre lettres
repris sur chaque colonne : `template_setting` avec `tpl_file`, `tpl_cre`… Les colonnes de
référence sont préfixées `ref_`.

L'intérêt apparaît dans les jointures : `id_data` seul est ambigu dès qu'on manipule
plusieurs tables, `tpl_cre` ne l'est jamais.

> **Pourquoi ne pas tout renommer ?** Il faudrait réécrire toutes les colonnes, tous les
> modèles qui les appellent et toute la documentation, à la main. Beaucoup de travail, aucun
> gain fonctionnel, et un risque élevé d'introduire des fautes de frappe dans du code qui
> fonctionne. La migration se fait progressivement : les colonnes nouvelles sont ajoutées
> avec la nouvelle convention, même dans les tables anciennes.

### Tables `_deleted`

Certaines tables ont une jumelle suffixée `_deleted` : `sigl_02_data` /
`sigl_02_deleted`. Une suppression déplace la ligne au lieu de l'effacer.

Attention, **aucune interface ne permet de restaurer** une ligne ainsi déplacée : c'est une
conservation, pas une corbeille. Une ligne absente de la table `_deleted` a été supprimée
manuellement en base.

### Colonnes de date

Les tables récentes portent systématiquement une colonne de date de création, et parfois une
date de mise à jour pour les données sensibles. Les tables historiques n'en ont pas toujours
— on ne sait pas quand un prescripteur a été créé.

## 7.7 Ajouter une fonctionnalité

Le déroulé habituel :

1. **Le point d'entrée existe-t-il ?** Une page, un bouton, un appel externe.
2. **Front end** : ajouter ou modifier le template, et la route si nécessaire.
3. **URL** : déclarer la ressource dans `app/__init__.py`.
4. **Service** : créer la classe dans le `*Rest.py` du domaine, avec le bon verbe.
5. **Modèle** : ajouter la fonction SQL — ou réutiliser une existante, comme le fait
   `DoctorExport`.
6. **Base** : si le schéma change, écrire un niveau Alembic (chapitre
   [06](06-migrations-alembic.md)).
7. **Traductions** : `extract`, `update`, `compile` si vous avez ajouté du texte visible.
8. **Tester** avant de livrer, en particulier toute requête SQL touchée.
