# Manuel de développement LabBook

Ce manuel s'adresse à un développeur qui rejoint le projet LabBook et doit être capable
d'installer un environnement de développement, de comprendre l'organisation du code, et
d'y apporter des évolutions.

Il couvre le conteneur, la base de données, le front end et le back end.

## Prérequis du lecteur

Python, SQL, HTML/CSS/JavaScript et la ligne de commande Linux. Le manuel n'enseigne ni
Flask, ni Jinja, ni Podman : il explique comment LabBook les utilise.

## Chapitres

| # | Chapitre | Contenu |
|---|---|---|
| [00](00-architecture.md) | Vue d'ensemble | Séparation front end / back end, rôle du conteneur |
| [01](01-environnement-de-developpement.md) | Environnement de développement | Prérequis, `labbook.conf`, base de données, premier lancement |
| [02](02-makefile-et-dockerfile.md) | Makefile et Dockerfile | Les cibles `make`, la construction de l'image |
| [03](03-storage-et-logs.md) | Le volume `storage` et les logs | Ce qui persiste, quel log pour quelle erreur |
| [04](04-front-end.md) | Développer côté front end | Routes, templates, Jinja, macros, formulaires dynamiques |
| [05](05-traductions.md) | Traductions | pybabel, catalogues, traductions stockées en base |
| [06](06-migrations-alembic.md) | Migrations Alembic | Créer et jouer un niveau de migration |
| [07](07-back-end.md) | Développer côté back end | Ressources REST, modèles, conventions SQL |
| [08](08-oauth2.md) | OAuth2 et sécurité de l'API | Clients, codes, jetons, portées |
| [09](09-exploitation.md) | Automatismes, scripts, HTTPS, débogage | Tâches planifiées, sauvegarde, recherche d'erreur |

## Version de référence

Ce manuel décrit LabBook **3.6.20** (tag `v3.6.20`, commit `d9f19c2`).

Les chemins de fichiers, les noms de fonctions et les rares numéros de ligne cités renvoient à
cette version. Les chemins et les noms restent valables longtemps ; **les numéros de ligne, non**
— au moindre ajout dans un fichier ils se décalent. Prenez-les comme un point de départ, et
confirmez toujours par une recherche sur le nom de la fonction ou de la variable.

## Convention

Les chemins de fichiers sont donnés depuis la racine du dépôt, par exemple
`labbook_BE/app/models/Doctor.py`. Les encadrés **Piège** signalent une erreur fréquente.
