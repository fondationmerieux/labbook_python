# 02 — Makefile et Dockerfile

Deux fichiers à la racine du dépôt commandent tout le cycle de construction et de
lancement. Le `Makefile` est le point d'entrée du développeur ; le `Dockerfile` décrit ce
qu'il y a dans l'image.

## 2.1 Le Makefile

Son but est d'éviter d'avoir à retenir de longues commandes `podman`, `mysql` ou `git`. Il
s'organise en quatre parties : variables globales, chargement de la configuration,
préparation de l'environnement, cibles.

### Chargement de la configuration

Le `Makefile` lit `labbook.conf` puis vérifie que les cinq variables indispensables sont
présentes (`Makefile:24-44`). S'il en manque une, il s'arrête net :

```
*** LABBOOK_DB_USER undefined. Stop.
```

C'est délibéré : mieux vaut un arrêt franc qu'un environnement à moitié monté qui échouera
plus loin, de façon plus obscure.

Toutes les variables de `labbook.conf` sont ensuite transmises au conteneur sous forme de
variables d'environnement, à sa création. Les applications les relisent au démarrage.

> **Conséquence.** Modifier `labbook.conf` n'a aucun effet sur un conteneur déjà lancé.
> Il faut `make devstop && make devrun`.

### Pod, conteneur, volumes

`make devrun` crée d'abord un **pod** podman nommé `labbook`
(`Makefile:46`, `Makefile:193`). Un pod regroupe plusieurs conteneurs qui partagent le même
réseau. Aujourd'hui LabBook n'en met qu'un, mais c'est ce pod qui permettra à LabBook
Connect de dialoguer avec lui.

Il prépare ensuite le stockage : `storage/` du dépôt est **recopié** (`rsync`) vers
`DEVRUN_STORAGE` — par défaut `./devrun_storage` — et c'est la copie qui est montée. Le
répertoire `storage/` versionné n'est donc jamais modifié par l'application.

Quatre répertoires de code sont montés en direct (`Makefile:78-81`) :

```
labbook_FE/app
labbook_BE/app
labbook_BE/alembic
labbook_BE/script
```

### Les cibles

Cibles de développement, toutes préfixées `dev` :

| Cible | Effet |
|---|---|
| `make devbuild` | construit `localhost/labbook-python:latest` depuis le répertoire de travail |
| `make devrun` | crée le pod, prépare stockage et logs, démarre le conteneur, monte les volumes → http://localhost:5000/sigl |
| `make devstop` | arrête et supprime le pod et le conteneur ; les données des volumes sont conservées |
| `make devclean` | supprime l'image de développement |

Cibles de base de données :

| Cible | Effet |
|---|---|
| `make dbtest` | teste uniquement la connexion MySQL avec les paramètres de `labbook.conf`. Ne vérifie pas le schéma. |
| `make dbinit` | **écrase** la base nommée dans `LABBOOK_DB_NAME` et la recharge depuis `etc/sql/demo_dump.sql` |

Cibles de livraison, à ne pas confondre avec les précédentes :

| Cible | Effet |
|---|---|
| `make build VERSION=x.y.z` | construit une image depuis le **tag git `vx.y.z`**, pas depuis le répertoire de travail |
| `make save VERSION=x.y.z` | exporte l'image en `.tar`, la compresse en `.tar.xz` et calcule les empreintes MD5 |
| `make clean VERSION=x.y.z` | supprime l'image de cette version |

> **Piège — `make build` et le tag git.** `make build` sort les sources du dépôt au tag
> `vx.y.z`, pas du répertoire courant. Si vous avez produit plusieurs itérations d'une même
> version, assurez-vous que le tag pointe bien sur le dernier commit poussé, sinon vous
> livrerez une image obsolète sans vous en apercevoir.

`make save` compresse en XZ : comptez un bon quart d'heure, mais l'archive passe d'environ
2,4 Go à 700 Mo.

## 2.2 Le Dockerfile

29 instructions, qui transforment un Linux minimal en serveur LabBook complet.

### Le système de base

```dockerfile
FROM almalinux:9.7
```

AlmaLinux a été retenu pour sa licence, sa légèreté et sa stabilité. La version est figée :
une version plus récente changerait les versions de paquets disponibles et les dépendances
associées.

À partir de cette ligne, considérez que vous disposez d'un serveur Linux neuf.

### Les logiciels installés

| Logiciel | Pourquoi |
|---|---|
| Python 3.11 | exécute les deux applications |
| Apache | serveur web, proxy vers les gunicorn |
| LibreOffice (headless) + unoconv | conversion ODT → PDF pour les comptes rendus |
| client MySQL | sauvegarde et restauration |
| wkhtmltopdf | rendu HTML → PDF (paquet non standard, fourni dans `vendor/`) |
| supervisor | pilote tous les services |

Le `Dockerfile` contient aussi des exclusions de paquets explicites — par exemple
`mysql-8.4-community-release`, qui s'installerait par défaut mais est mal compatible avec
cette version d'AlmaLinux. Ce genre de ligne est le résultat d'un test, pas un choix
théorique : ne les retirez pas sans vérifier.

### unoconv et le coût du premier PDF

`unoconv` lance LibreOffice en arrière-plan. Comme tout démarrage de LibreOffice, ce n'est
pas instantané : **la première conversion ODT → PDF après le lancement du conteneur prend 5
à 10 secondes**. Les suivantes sont immédiates. Ce n'est pas un bug, et c'est visible par
l'utilisateur.

Une alternative, `unoserver`, démarrerait au lancement du conteneur plutôt qu'à la première
utilisation, et déplacerait donc cette attente. Elle n'est pas retenue à ce jour : elle
réclame une bibliothèque Python que la version fournie par AlmaLinux 9 ne satisfait pas, ce
qui rendrait le conteneur dépendant du socle — exactement ce que le conteneur est censé
éviter.

### Ce que fait le reste du fichier

- création des répertoires attendus par l'application, dont ceux du stockage ;
- copie du contenu initial de `storage/` et des ressources ;
- copie des configurations Apache, supervisor et logrotate ;
- un lien symbolique de `storage/resource` vers l'arborescence publiée par Apache, qui
  permet de servir une ressource stockée sans la recopier ailleurs ;
- copie des sources FE et BE, puis création d'un environnement virtuel Python pour chacune
  (`Dockerfile:68` et `Dockerfile:79`) ;
- enfin, `CMD supervisord`, l'unique processus du conteneur.

## 2.3 Quand faut-il reconstruire

C'est la question pratique la plus fréquente.

**Pas de reconstruction** — les quatre répertoires montés par `make devrun` :
`labbook_FE/app`, `labbook_BE/app`, `labbook_BE/alembic`, `labbook_BE/script`. Pour un
template, rafraîchir la page suffit ; pour du Python, `LABBOOK_DEBUG=1` fait relancer
gunicorn via `--reload`.

**Redémarrage seul** (`make devstop && make devrun`) : une nouvelle migration Alembic —
Alembic ne s'exécute qu'au démarrage — et tout changement de `labbook.conf`.

**Reconstruction** (`make devbuild`) : `Dockerfile`, `Pipfile`, `default_settings.py`,
configurations Apache et supervisor, contenu de `storage/`, et `labbook_BE/script/backup.sh`.

> **Piège — `backup.sh`.** Ce fichier est pourtant dans un répertoire monté. Mais
> `backup.sh` lance des conteneurs frères qui, eux, n'héritent pas des montages : ils voient
> la version présente dans l'image. Toute modification de `backup.sh` exige un `make devbuild`.

Enfin, `make devclean` invalide le cache : le `devbuild` suivant refait les 29 étapes,
téléchargement de LibreOffice compris. À réserver aux cas où vous voulez repartir propre.
