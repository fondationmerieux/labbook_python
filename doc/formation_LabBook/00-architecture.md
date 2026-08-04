# 00 — Vue d'ensemble

## Ce qu'est LabBook

LabBook est un logiciel de gestion de laboratoire de biologie médicale (LIMS). Il gère les
patients, les dossiers d'analyse, la saisie et la validation des résultats, l'édition des
comptes rendus, la facturation, le contrôle qualité et l'export de données vers des
plateformes tierces.

Il est livré sous forme d'**image de conteneur**, déployée sur une installation Ubuntu
dédiée. Les données structurées vont dans MySQL ou MariaDB ; les fichiers (comptes rendus,
pièces jointes, ressources) vont sur un volume de stockage.

Le logiciel est publié sous licence **GPL v2**. Toute redistribution — y compris d'une
version dérivée — impose la publication des sources modifiées. L'usage interne à une
organisation, lui, n'impose rien.

## Deux applications, pas une

Le dépôt contient **deux applications Flask distinctes**, empaquetées dans une seule image :

| | Rôle | Port |
|---|---|---|
| `labbook_FE` | Front end : pages HTML rendues côté serveur (Jinja2), sessions, appels au back end | 8081 |
| `labbook_BE` | Back end : API REST (Flask-RESTful) branchée directement sur MySQL | 8082 |

Elles ne partagent pas de code. **Le front end n'accède jamais à la base de données** : il
interroge le back end en HTTP, même si les deux tournent dans le même conteneur.

Cette séparation est historique. La version 2.x de LabBook était écrite en PHP ; la
migration vers Python s'est faite page par page, ce qui a imposé de disposer d'un front end
avant que le back end existe. Le découpage est resté. Un projet démarré aujourd'hui
n'aurait pas de raison de le reproduire — mais il structure tout le code existant, et c'est
la première chose à intégrer avant de lire quoi que ce soit.

### Le trajet d'une requête

```
Navigateur
   ↓  HTTP  /sigl/...
Apache (dans le conteneur)
   ↓  proxy
gunicorn FE :8081   →  labbook_FE/app/__init__.py   (182 routes)
   ↓  HTTP + jeton OAuth2  /services/...
gunicorn BE :8082   →  labbook_BE/app/__init__.py   (290 ressources REST)
   ↓
labbook_BE/app/services/*Rest.py     ← reçoit, valide, trace
   ↓
labbook_BE/app/models/*.py           ← écrit le SQL
   ↓
MySQL / MariaDB (sur la machine hôte)
```

Le préfixe `/sigl` présent dans toutes les URLs permet à Apache de router vers LabBook et
de cohabiter avec d'autres applications sur la même machine.

## Ce qui tourne dans le conteneur

Un conteneur n'exécute qu'un processus principal. Ici c'est **supervisor**, qui démarre et
surveille cinq services (`supervisor/etc/`) :

| Service | Rôle |
|---|---|
| `apache` | reçoit les requêtes et fait le proxy vers les deux gunicorn |
| `gunicorn_fe` | le front end |
| `gunicorn_be` | le back end |
| `automation_runner` | tâches planifiées, hors gunicorn (chapitre [09](09-exploitation.md)) |
| `logrotate_labbook` | rotation hebdomadaire des logs |

Si l'un s'arrête, supervisor le relance.

### Ordre de démarrage

Il n'est pas libre, et il n'est pas intuitif :

1. **Le front end démarre en premier.** Son `gunicorn.sh` génère, si absents, deux secrets
   dans `/storage/key/` : `secret_key.py` (chiffrement des sessions Flask) et
   `oauth_client_secret.py`.
2. **Le back end attend.** Son `gunicorn.sh` bloque tant que le port 8081 ne répond pas et
   tant que le secret OAuth n'est pas écrit (`labbook_BE/gunicorn.sh:76-139`).
3. Le back end lance ensuite `alembic upgrade head` pour mettre la base à niveau.
4. Puis seulement il démarre gunicorn sur 8082.

Ces secrets sont générés **une fois par installation** et partagés par les deux
applications. Ils doivent être identiques des deux côtés, sinon les sessions et les jetons
OAuth ne sont pas interprétables d'un côté à l'autre.

## Pourquoi un conteneur

Le socle Linux varie d'un site à l'autre ; le contenu du conteneur, non. Le `Dockerfile`
fige la version d'AlmaLinux, celle de Python, et celles de LibreOffice, wkhtmltopdf et du
client MySQL dont dépend LabBook. Les développeurs travaillent sur le même environnement
que la production.

Conséquence à ne jamais perdre de vue : **le conteneur est immuable**. Une modification
faite à l'intérieur — éditer un fichier, corriger une traduction — disparaît au premier
redémarrage. Tout changement durable passe par une nouvelle image, ou par une migration
Alembic pour ce qui touche la base et le stockage.

C'est aussi pour cela que le stockage et les logs sont montés depuis l'extérieur : ils
doivent survivre au conteneur.

## Organisation du dépôt

| Chemin | Contenu |
|---|---|
| `labbook_FE/app/` | front end : `__init__.py`, `templates/`, `static/`, `models/`, `translations/` |
| `labbook_BE/app/` | back end : `__init__.py`, `services/`, `models/`, `security/`, `automation/` |
| `labbook_BE/alembic/` | migrations de base de données |
| `labbook_BE/script/` | scripts shell (sauvegarde, restauration, échanges automates) |
| `Dockerfile`, `Makefile` | construction et lancement |
| `storage/` | contenu initial du volume permanent |
| `etc/sql/demo_dump.sql` | base de démonstration |
| `apache/`, `supervisor/`, `logrotate.d/` | configuration des services du conteneur |
| `doc/` | documentation technique (tables, sauvegarde, exports, dépendances) |

Les répertoires qui comptent au quotidien sont `labbook_FE/app` et `labbook_BE/app`.

## Documentation existante

Ce manuel ne remplace pas les documents de `doc/`, qui restent la référence sur leurs
sujets :

| Fichier | Sujet |
|---|---|
| `doc/architecture.md` | architecture de production |
| `doc/tables.md` | les 119 tables de la base |
| `doc/backup_api.md` | contrat d'appel de `backup.sh` |
| `doc/dhis2.md`, `doc/epidemio.md`, `doc/indicator.md` | formats d'export |
| `doc/import.md` | schémas d'import |
| `doc/customizable_form.md` | syntaxe des formulaires paramétrables |
| `doc/dependencies.md` | bibliothèques tierces et licences |
