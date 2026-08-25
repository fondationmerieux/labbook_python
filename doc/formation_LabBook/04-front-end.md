# 04 — Développer côté front end

Le front end rend des pages HTML côté serveur avec Jinja2, gère la session, et va chercher
toutes ses données auprès du back end en HTTP. Il n'ouvre **jamais** de connexion à la base.

## 4.1 Organisation

```
labbook_FE/
├── Pipfile              dépendances Python
├── gunicorn.sh          script de lancement
└── app/
    ├── __init__.py      l'application : configuration, fonctions communes, 182 routes
    ├── templates/       187 templates Jinja
    ├── static/          ressources statiques (img, js, vendor)
    ├── models/          Form.py, Constants.py, Logs.py
    ├── translations/    catalogues de traduction
    └── babel.cfg        configuration d'extraction des chaînes
```

### Le Pipfile

Les dépendances sont gérées avec `pipenv`, qui résout les versions de façon cohérente entre
paquets — là où un `requirements.txt` laisserait s'installer des combinaisons
incompatibles.

| Paquet | Rôle |
|---|---|
| `flask`, `werkzeug`, `jinja2` | le socle web |
| `gunicorn` | serveur d'application |
| `babel`, `flask-babel` | traductions |
| `requests`, `urllib3` | appels HTTP vers le back end |
| `tomli` | lecture de fichiers TOML |
| `pip-audit` | audit de vulnérabilités des dépendances, hors exécution |

Les versions sont **encadrées** (`>=3.1.3, <3.2.0`) et non simplement minorées : une version
majeure non testée ne doit pas s'installer toute seule.

`pip-audit` s'exécute à la main, depuis l'environnement virtuel, et signale les paquets
porteurs de vulnérabilités connues.

### gunicorn.sh

Il prépare l'environnement avant de lancer gunicorn :

1. crée les répertoires manquants ;
2. génère `secret_key.py` s'il n'existe pas — la clé de chiffrement des sessions, unique par
   installation ;
3. génère `oauth_client_secret.py` ;
4. crée `local_settings.py` depuis son modèle et y injecte la clé partagée ;
5. lance gunicorn, avec `--reload` si `LABBOOK_DEBUG=1`.

Ce fichier ne se touche pratiquement jamais.

### Les fichiers de configuration

- `default_settings.py` : le numéro de version, rien d'autre.
- `local_settings.py` (créé depuis `.sample`) : clés secrètes, mode debug, durée de session
  (un jour), langue par défaut, préfixe d'URL.

L'ordre de résolution est : `default_settings.py`, puis `local_settings.py`, puis les
variables d'environnement, qui l'emportent.

## 4.2 Le fichier `__init__.py`

Près de **8 500 lignes**. Il se lit en trois zones.

### Zone 1 — Initialisation (jusqu'à la ligne ~1000)

Imports, liste des langues, préparation des logs — la première chose faite, pour que tout ce
qui suit puisse être tracé —, création de l'application Flask, chargement des réglages,
configuration de la session, initialisation d'OAuth2 et de Babel.

### Zone 2 — Fonctions communes

**Préprocesseurs** (`@app.context_processor`, `@app.before_request`) : vérification de la
langue, contrôle du délai d'inactivité, redirection vers la déconnexion. Exécutés avant
chaque requête, invisibles pour l'utilisateur.

**Helpers OAuth2** : récupération et rafraîchissement du jeton. Regroupés une fois pour
toutes plutôt que réécrits à chaque appel.

**Filtres de template** (`@app.template_filter`) : essentiellement du formatage de dates.
Écrire `{{ ma_date | date_format }}` dans un template fait exécuter la fonction côté
serveur. C'est délibéré : manipuler des dates en Python est plus simple et plus fiable
qu'en JavaScript.

**`get_init_var()` et `get_user_data()`** : au moment de la connexion, le front end
interroge le back end pour les valeurs dont il aura besoin en permanence — délai de
déconnexion, langue par défaut, profil et droits de l'utilisateur, couleurs de
personnalisation, format des numéros de dossier — et les range en session. Elles ne sont pas
redemandées à chaque page.

**Construction de chemins sécurisés** : le front end construit parfois un chemin de fichier
à partir d'une information venue du back end. Une fonction dédiée encadre cette
construction pour empêcher qu'un paramètre manipulé fasse sortir de l'arborescence
autorisée.

### Zone 3 — Les routes (l'essentiel du fichier)

182 routes, déclarées avec `@app.route(...)`, dans cet ordre : routes OAuth, `/` (index),
page de connexion, page d'accueil, puis toutes les pages métier, et enfin les routes
particulières en fin de fichier.

> **Convention.** Les nouvelles fonctions ne sont pas ajoutées à la fin du fichier mais
> dans leur section. Respectez-la, sinon le fichier devient inutilisable.

### Structure type d'une route

Presque toutes les routes suivent le même schéma :

```python
@app.route('/home_page')
def home_page():
    log.info(Logs.fileline() + ' : TRACE home_page')   # 1. tracer l'entrée
    session['current_page'] = 'home_page'              # 2. mémoriser la page courante
    session.modified = True

    resp = ensure_be_token()                           # 3. s'assurer d'avoir un jeton
    if resp:                                           #    sinon partir vers OAuth
        return resp

    args = {}                                          # 4. préparer le conteneur de données

    data, redir = be_get('/services/…', 'home data')   # 5. interroger le back end
    if redir:                                          # 6. jeton expiré : repartir vers OAuth
        return redir
    if data is not None:                               # 7. exploiter la réponse
        args['data'] = data

    return render_template('home-page.html',           # 8. rendre le template
                           args=args, rand=secrets.randbelow(1000))
```

Quelques points :

- **la mémorisation de la page courante** permet de revenir où l'on était après un
  rafraîchissement ;
- **`be_get(chemin, libellé)` et `be_post(chemin, corps, libellé)`** portent tous les appels au
  back end : ils construisent l'URL, posent l'en-tête d'autorisation, appliquent le délai de
  10 secondes, tracent l'appel sous le `libellé` donné, et renvoient le couple
  `(données, redirection)` ;
- **`données` vaut `None`** dès que l'appel n'aboutit pas, ce qui laisse à l'appelant sa propre
  valeur par défaut — d'où le `if data is not None` avant d'affecter ;
- **`redirection` n'est renseignée que si le jeton a expiré** ; l'appelant la retourne
  immédiatement, ce qui relance la séquence OAuth. Les autres erreurs ne provoquent pas de
  redirection : elles sont tracées et la page s'affiche sans ces données ;
- **le nombre aléatoire `rand`** passé au template contourne des mises en cache trop zélées
  de certains navigateurs, qui réaffichaient l'ancienne page après une modification. Il vient
  de `secrets`, et non de `random`, dont le générateur n'offre aucune garantie.

Une même vue peut porter plusieurs routes, avec ou sans argument typé :

```python
@app.route('/home_page')
@app.route('/home_page/<string:login>')
```

## 4.3 Templates

### Nommage

| Préfixe | Rôle | Nombre |
|---|---|---|
| `list-` | vues liste / grille | 36 |
| `det-` | formulaires de détail (*detail*) | 33 |
| `setting-` | pages d'administration | 30 |
| `report-` | écrans de rapport | 7 |
| `res-` | résultats de contrôle | 2 |

Plus `templates/popup/` (fenêtres modales), `templates/js/` (JavaScript à rendre
dynamiquement), `templates/elem/` (éléments des formulaires paramétrables), et `macros.html`.

> **À savoir.** Tout ce qui est sous `templates/` est passé à la moulinette Jinja. Tout ce
> qui est sous `static/` est servi tel quel. C'est le seul critère.

### Les morceaux partagés

Un fragment identique répété dans plusieurs pages est sorti dans son propre fichier, inclus
par chacune. `templates/js/` en compte une quinzaine — libellés des tableaux DataTables,
recherche d'analyse, dépôt et suppression de pièce jointe, réinitialisation d'un résultat,
filtre LabBook Lite — et le même principe s'applique au HTML : `patient-identity.html`
(identité du patient), `lite-filter.html` (le filtre lui-même), `patient-header.html`.

Ces fichiers commencent par un commentaire Jinja `{# … #}` qui dit ce qu'ils attendent de
l'appelant. Quand un paramètre est nécessaire, il est posé juste avant l'inclusion :

```jinja
{% set result_return_page = 'technical-validation' %}
{% include 'js/result_reset_cancel.js' %}
```

> **Piège.** Sortir un bloc dans un fichier neuf ne réduit la duplication que si **toutes**
> ses copies sont remplacées. Il en reste une ailleurs et le compte augmente, le nouveau
> fichier s'ajoutant aux occurrences déjà présentes.

### `static/`

```
static/img/       icônes et logos
static/js/        JavaScript commun, non dynamique
static/vendor/    bibliothèques tierces
```

`vendor/` contient Bootstrap 5.1, jQuery, DataTables, Chart.js, Moment, select2, swagger-ui,
les polices Font Awesome. Ces bibliothèques ne sont **pas** installées par un gestionnaire de
paquets : ce sont des fichiers versionnés dans le dépôt (voir `doc/dependencies.md`).

Bootstrap est volontairement resté en 5.1 : monter de version imposerait de revérifier le
rendu des 132 pages.

## 4.4 `skeleton.html`, le gabarit

Toutes les pages en héritent, sauf trois : la page de connexion, la page des contributeurs
et la page API. Il définit :

- le sens d'écriture, inversé automatiquement quand la locale est l'arabe ;
- le chargement des bibliothèques communes ;
- l'en-tête (logo, menu, bloc utilisateur, sélecteur de langue) ;
- le pied de page (numéro de version, lien contributeurs) ;
- les fenêtres modales communes (« veuillez patienter », succès, erreur) ;
- le JavaScript commun : déconnexion sur inactivité, téléchargement de fichier, relève des
  messages non lus toutes les 30 secondes ;
- le jeton OAuth, pour que les appels Ajax puissent s'authentifier.

`select2`, plus lourde, n'est chargée que par les pages qui en ont besoin.

### Héritage

```jinja
{% extends "skeleton.html" %}

{% block head %}
  {{ super() }}                          {# conserve le contenu du gabarit #}
  <link rel="stylesheet" href="...">     {# et ajoute le sien #}
{% endblock %}

{% block content %}
  ...
{% endblock %}
```

> **Piège — `{{ super() }}`.** Sans lui, vous **écrasez** le bloc du gabarit au lieu de le
> compléter. Toutes les bibliothèques communes disparaissent, et la page casse de façon peu
> explicite.

Pour le JavaScript, on n'étend pas le bloc `script` du gabarit : on ouvre un **second bloc**
`addscript`. Une page peut porter plusieurs blocs de script, et la surcharge se comporte
mal ici.

## 4.5 Jinja en pratique

Trois syntaxes à distinguer, souvent mêlées dans le même fichier avec du HTML et du
JavaScript :

| Syntaxe | Rôle |
|---|---|
| `{{ valeur }}` | insère une valeur |
| `{% if %}`, `{% for %}` | logique — toujours refermée par `{% endif %}`, `{% endfor %}` |
| `{{ _("texte") }}` | marque une chaîne à traduire (chapitre [05](05-traductions.md)) |

Jinja est **exécuté par le serveur**. Ce que vous ne faites pas en Jinja, vous le ferez en
JavaScript côté client : c'est un arbitrage entre la charge du serveur et celle du poste de
l'utilisateur. En pratique, le poste est souvent le maillon faible, ce qui pousse à préparer
le maximum côté serveur.

### Macros

Un bloc réutilisable, défini dans `macros.html` :

```jinja
{% from "macros.html" import select_analysis %}
{{ select_analysis(args.list_analysis) }}
```

Typiquement pour préremplir une liste déroulante : la route a déjà chargé les données, la
macro construit les `<option>`. On évite ainsi un appel JavaScript supplémentaire au
chargement de la page.

Une macro se justifie quand l'élément sert à plusieurs endroits. Pour un cas unique, une
boucle `{% for %}` écrite directement dans la page est plus lisible.

## 4.6 Routes qui servent des ressources dynamiques

Le CSS et certains JavaScript doivent contenir des chaînes traduites ou des couleurs
personnalisées. Ils ne peuvent donc pas être statiques : ils sont servis par une route,
comme un template. C'est le cas de `app-labbook.css`, du JavaScript de `templates/js/` et de
`app-swagger-api.yaml`.

## 4.7 Gestion de fichiers

Trois routes : téléchargement, dépôt, suppression. Elles renvoient du **JSON**, pas une
page : elles sont appelées par un bouton, elles ne font pas naviguer.

Chacune reçoit un **type** et une **référence**, qui déterminent le répertoire cible et le
traitement (nom en clair ou empreinte). La liste des types autorisés est **énumérée
explicitement** dans le code : une liste ouverte serait une porte d'entrée, et les outils
d'analyse de sécurité la signalent comme telle.

> **Piège — le type manquant.** Si vous ajoutez un nouveau type de fichier et que le
> téléchargement ne fonctionne pas sans erreur claire, vérifiez d'abord que le type figure
> bien dans la liste autorisée.

Les noms de fichiers et les chemins sont filtrés (lettres, chiffres, `_`, `-`), pour
interdire caractères joker et remontées d'arborescence.

> **En développement.** Chrome bloque les téléchargements depuis un site non HTTPS et exige
> une confirmation. On croit que le téléchargement a échoué alors qu'il attend un clic.
> Firefox ne se comporte pas ainsi. En production sur HTTPS, le problème disparaît.

## 4.8 Formulaires paramétrables

Deux pages ne sont pas des templates ordinaires : la **fiche patient** et l'**historique
patient**. Leur contenu est décrit par un fichier de configuration modifiable depuis
l'interface (*Configuration de formulaire*), ce qui permet à chaque laboratoire d'ajouter
ses propres champs sans nouvelle version du logiciel.

Le fichier comporte deux sections : `description` (la liste des éléments) et `layout` (leur
mise en page). La syntaxe est documentée dans `doc/customizable_form.md` et
`doc/patient_history_form_spec.md`.

Les éléments réutilisables — sélecteur de date, liste déroulante, zone de texte, boutons
radio — sont des mini-templates de `templates/lm/`. Les champs prédéfinis sont préfixés
`pat_`.

Le rendu passe par **deux moulinettes successives** :

1. le code lit la description et engendre du HTML et du JavaScript, qui contiennent encore
   du Jinja ;
2. ce résultat repasse dans Jinja, ce qui résout les traductions ;
3. le tout est injecté dans `det-patient.html`, qui est un template classique.

C'est le mécanisme le plus enchevêtré du front end. Il n'a pas besoin d'être maîtrisé pour
travailler ailleurs, mais il faut savoir qu'il existe : ces deux pages ne se modifient pas
comme les autres.

## 4.9 Déboguer le front end

Le HTML et le JavaScript ne sont pas validés au chargement, contrairement à Python. Une
accolade manquante ne se manifeste qu'à l'exécution, et souvent **loin de son origine** : le
navigateur signale la dernière ligne du fichier, parce que c'est là qu'il constate le
déséquilibre.

Les erreurs de template sont donc rarement difficiles à corriger, mais souvent difficiles à
localiser. Le réflexe le plus efficace n'est pas l'inspecteur du navigateur, dont
l'indication de ligne est peu fiable ici : c'est de regarder dans git ce qui a changé
récemment.

Les pages complexes — saisie de résultats, validation biologique — concentrent beaucoup de
JavaScript et beaucoup de guillemets simples et doubles. Ce sont celles qui cassent le plus
facilement.
