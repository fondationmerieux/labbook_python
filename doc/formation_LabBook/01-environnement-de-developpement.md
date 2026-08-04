# 01 — Monter son environnement de développement

L'environnement de développement reproduit l'environnement de production : l'application
tourne dans un conteneur, et se connecte à une base de données qui, elle, tourne sur la
machine hôte. C'est le point le plus important à comprendre avant de commencer, parce que
la quasi-totalité des difficultés d'installation vient de là : **le conteneur et vous ne
voyez pas la base de données à la même adresse**.

La différence avec la production tient en deux points :

- certains répertoires du dépôt sont montés en direct dans le conteneur, donc une
  modification de code est visible sans reconstruire l'image ;
- le volume de stockage permanent, qui est un vrai volume en production, est ici un simple
  répertoire de votre disque.

## 1.1 Prérequis

| Élément | Version |
|---|---|
| Linux | Ubuntu 22.04 ou 24.04 (autres distributions possibles, non testées) |
| Podman | — |
| MySQL | 8.4+ **ou** MariaDB 10.3+ |
| make | — |
| git | — |

```bash
sudo apt update
sudo apt install -y podman mysql-server make git
```

Si MySQL est déjà installé sur votre poste, ne le réinstallez pas : retirez simplement
`mysql-server` de la ligne. LabBook créera une base supplémentaire à côté des vôtres, sans
toucher aux autres.

> **Piège — architecture processeur.** Le `Dockerfile` part d'une image `almalinux:9.7`
> x86-64. Sur un Mac Apple Silicon, une machine virtuelle Ubuntu ARM ne pourra pas
> construire l'image : le build échoue à la résolution des paquets. Il n'existe pas de
> contournement rapide, le portage ARM demanderait de retravailler le `Dockerfile`.
> Utilisez une machine x86-64.

### Cas particulier : poste installé depuis l'ISO LabBook

Si vous partez d'une machine installée avec l'ISO LabBook plutôt que d'un Ubuntu vierge,
trois choses en plus, avant tout le reste.

Arrêter le service LabBook du socle, qui occuperait les mêmes ports :

```bash
sudo systemctl stop labbook
sudo mv /etc/init.d/labbook /etc/init.d/labbook.O   # désactive le démarrage automatique
```

Restaurer les dépôts Ubuntu — l'ISO les bloque volontairement pour figer les versions de
paquets, ce qui vous empêcherait d'installer `git` :

```bash
sudo tee -a /etc/apt/sources.list <<EOF

deb http://archive.ubuntu.com/ubuntu jammy main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu jammy-updates main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu jammy-backports main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu jammy-security main restricted universe multiverse

EOF
```

Et, si nécessaire, désactiver le pare-feu qui bloquerait le port 3306 :

```bash
sudo systemctl disable ufw && sudo systemctl stop ufw
```

## 1.2 Récupérer les sources

```bash
cd $HOME
git clone https://github.com/fondationmerieux/labbook_python.git
cd labbook_python
```

Comptez environ 300 Mo et beaucoup de petits fichiers.

> **Piège — le clone au mauvais endroit, en root.** Écrire `cd /home` au lieu de
> `cd $HOME` vous place dans le répertoire partagé de tous les utilisateurs, où vous n'avez
> pas le droit d'écrire. Le `git clone` échoue, la tentation est alors de le relancer avec
> `sudo` — et là il réussit, mais le dépôt appartient à `root:root`. Tout casse ensuite, à
> commencer par `make devbuild` qui n'arrive plus à créer ses répertoires.
>
> Aucune commande de ce chapitre ne demande `sudo`, à l'exception de `apt install`.
> Si vous avez déjà fait l'erreur :
>
> ```bash
> cd $HOME
> sudo mv /home/labbook_python .
> sudo chown -R $USER:$USER labbook_python
> ```

## 1.3 Le fichier de configuration

LabBook lit sa configuration dans un fichier `labbook.conf`, cherché à deux emplacements :

- `$HOME/.config/labbook.conf`
- `$HOME/labbook.conf`

Partez du modèle fourni :

```bash
cp doc/labbook.conf.sample $HOME/.config/labbook.conf
```

Cinq variables sont **obligatoires** : sans elles, le `Makefile` s'arrête immédiatement
(`Makefile:24` à `Makefile:44`) avec un message du type
`*** LABBOOK_DB_USER undefined. Stop.` C'est volontaire — mieux vaut un arrêt net qu'un
environnement à moitié monté.

| Variable | Rôle |
|---|---|
| `LABBOOK_DB_USER` | utilisateur de la base |
| `LABBOOK_DB_PWD` | son mot de passe |
| `LABBOOK_DB_NAME` | nom de la base (par convention `SIGL`) |
| `LABBOOK_DB_HOST` | **adresse de la base telle que le conteneur la voit** |
| `LABBOOK_DEBUG` | `1` pour lancer gunicorn avec `--reload` |

Les autres sont optionnelles, avec des valeurs par défaut :

| Variable | Rôle |
|---|---|
| `LABBOOK_ROOTLESS` | `1` si vous lancez podman sans `sudo` — évite d'avoir à préfixer toutes les commandes |
| `DEVRUN_STORAGE` | où placer le stockage de développement (défaut `./devrun_storage`) |
| `LABBOOK_URL_PREFIX` | remplace `sigl` dans les URLs |
| `LABBOOK_USER` | remplace `user_labbook` pour la sauvegarde/restauration |
| `LABBOOK_MEDIA_DIR` | remplace `/media` pour les médias amovibles |
| `LABBOOK_TEST_OK` / `LABBOOK_TEST_KO` | simulent le succès ou l'échec de commandes de `backup.sh` |
| `LABBOOK_DUMP_COL_STATS` | `0` ajoute `--column-statistics=0` à `mysqldump` (nécessaire au-delà de mysqldump 8) |

> **Piège — les valeurs d'exemple du modèle.** `doc/labbook.conf.sample` livre
> `LABBOOK_DB_USER=myUser` et `LABBOOK_DB_PWD=myPass`. Ce sont des valeurs de démonstration,
> pas des valeurs par défaut fonctionnelles. Si vous les laissez telles quelles, `make dbinit`
> échoue sur un `Access denied`. Remplacez-les par un utilisateur qui existe réellement dans
> votre MySQL — sur un poste de développement, `root` / `root` convient très bien.

### Le cas de `LABBOOK_DB_HOST`

C'est la variable qui pose le plus de problèmes, parce que sa valeur dépend du mode dans
lequel tourne podman. Retenez qu'elle décrit l'adresse de la base **vue depuis l'intérieur
du conteneur**, jamais vue depuis votre terminal.

| Mode podman | Valeur |
|---|---|
| rootless (`LABBOOK_ROOTLESS=1`) | `host.containers.internal` |
| rootful | `10.88.0.1` |

> **Note.** `host.containers.internal` est un nom résolu par podman, qui suit la machine.
> Renseigner une adresse IP fixe fonctionne aussi, mais vous oblige, à chaque changement
> d'adresse, à modifier le fichier, à créer l'utilisateur MySQL correspondant, puis à
> relancer le conteneur (`make devstop && make devrun`) — ces variables ne sont transmises
> qu'à sa création.

Exemple de fichier complet pour un poste de développement rootless :

```ini
LABBOOK_DB_USER=root
LABBOOK_DB_PWD=root
LABBOOK_DB_NAME=SIGL
LABBOOK_DB_HOST=host.containers.internal
LABBOOK_DEBUG=1
LABBOOK_ROOTLESS=1
LABBOOK_URL_PREFIX=
LABBOOK_TEST_OK=
LABBOOK_TEST_KO=
LABBOOK_USER=
LABBOOK_MEDIA_DIR=
LABBOOK_DUMP_COL_STATS=
DEVRUN_STORAGE=
```

## 1.4 Préparer MySQL

Trois réglages serveur, puis la création des utilisateurs.

### Réglages serveur

Vider `sql_mode`, sans quoi le dump de démonstration ne se charge pas :

```ini
# MariaDB — /etc/my.cnf.d/mariadb-server.cnf, section [mariadb]
sql_mode=''
```

Autoriser les connexions venant d'ailleurs que de `localhost`, puisque le conteneur est un
« ailleurs » :

```ini
# MySQL — /etc/mysql/mysql.conf.d/mysqld.cnf
# bind-address = 127.0.0.1
bind-address = 0.0.0.0
```

Sur MySQL 8, aligner le mode d'authentification, dont le défaut a changé au fil des versions :

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'root';
FLUSH PRIVILEGES;
```

Redémarrez MySQL après modification des fichiers `.cnf`.

### Utilisateurs

Il faut autoriser **deux chemins d'accès distincts**, et c'est là que la plupart des
installations échouent : depuis le conteneur (pour l'application) et depuis l'hôte (pour
`make dbinit`, et pour vos propres requêtes).

```sql
-- avec LABBOOK_DB_USER=root et LABBOOK_DB_PWD=root

-- depuis le conteneur
CREATE USER 'root'@'10.88.%.%' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'10.88.%.%';

-- depuis l'hôte
CREATE USER 'root'@'localhost' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost';

FLUSH PRIVILEGES;
```

Si l'un de ces utilisateurs existe déjà, MySQL renvoie une erreur : c'est sans conséquence,
passez à la suivante.

Si vous avez choisi de renseigner une IP dans `LABBOOK_DB_HOST` plutôt que
`host.containers.internal`, ajoutez un troisième utilisateur pour cette adresse :

```sql
CREATE USER 'root'@'192.168.255.214' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'192.168.255.214';
FLUSH PRIVILEGES;
```

> **Piège — `blocked because of many connection errors`.** Après plusieurs tentatives de
> connexion refusées, MySQL bannit l'hôte fautif, et il continue de le refuser même une fois
> les droits corrigés. Le symptôme est déroutant : les droits sont bons, et pourtant le
> conteneur n'entre pas. Débloquez avec :
>
> ```sql
> FLUSH HOSTS;
> ```
>
> ou, depuis le shell : `mysqladmin -u root -p flush-hosts`.
> Pensez-y dès que les droits vous semblent corrects sans que la connexion passe.

## 1.5 Initialiser la base

```bash
cd $HOME/labbook_python
make dbtest   # vérifie uniquement la connexion, pas le schéma
make dbinit   # crée la base et la charge
```

`make dbinit` charge `etc/sql/demo_dump.sql` : c'est la base du
[site de démonstration](http://demo.lab-book.org/). Elle contient le schéma complet — 119
tables, décrites dans `doc/tables.md` — et le référentiel d'analyses, exactement comme une
base de production. La seule différence tient à la dizaine d'utilisateurs applicatifs déjà
créés (un administrateur, un biologiste, un technicien, une secrétaire…).

> `make dbinit` **écrase** la base nommée dans `LABBOOK_DB_NAME`. Des messages `DROP DATABASE`
> et des avertissements à l'exécution sont normaux ; seules les lignes `ERROR` méritent
> attention.

Vérification :

```sql
USE SIGL;
SELECT * FROM alembic_version;
```

Si la table répond, la base est en place. La valeur renvoyée est l'identifiant de la
dernière migration jouée — voir le chapitre [06](06-migrations-alembic.md).

## 1.6 Construire et lancer

```bash
make devbuild   # construit l'image depuis le répertoire de travail
make devrun     # démarre le pod et le conteneur
```

Le premier `devbuild` est long : environ 77 étapes, dont le téléchargement de LibreOffice
(près d'un giga). Les suivants réutilisent le cache. Une fois cette étape franchie, plus
rien ne se télécharge.

L'application répond alors sur **http://localhost:5000/sigl**.

Les autres cibles :

```bash
make devstop    # arrête et supprime le pod et le conteneur ; les données sont conservées
make devclean   # supprime l'image de développement
```

> `make devclean` force un `devbuild` complet au prochain lancement, LibreOffice compris.
> Ne l'utilisez que pour repartir d'un environnement propre.

## 1.7 Ce qui est rechargé à chaud, et ce qui ne l'est pas

`make devrun` monte quatre répertoires du dépôt directement dans le conteneur
(`Makefile:78` à `Makefile:81`) :

```
labbook_FE/app
labbook_BE/app
labbook_BE/alembic
labbook_BE/script
```

Une modification dans l'un d'eux est visible **sans reconstruire l'image**. Pour un template
ou une chaîne de caractères, rafraîchir la page suffit. Pour du code Python,
`LABBOOK_DEBUG=1` fait relancer gunicorn tout seul grâce à `--reload`.

Tout ce qui est en dehors de ces quatre répertoires demande un `make devbuild` : le
`Dockerfile`, les `Pipfile`, les `default_settings.py`, la configuration Apache et
supervisor, le contenu initial de `storage/`, et `labbook_BE/script/backup.sh` — ce dernier
parce qu'il est exécuté dans des conteneurs frères qui n'héritent pas des montages.

Cas particulier, celui d'un **niveau Alembic**. Le répertoire `labbook_BE/alembic` étant
monté, votre fichier de migration est bien vu par le conteneur sans reconstruction ; mais
Alembic ne s'exécute qu'au démarrage. Il faut donc redémarrer, sans rebuild :

```bash
make devstop && make devrun
```

> **Note.** `make devbuild` est inutile ici : `labbook_BE/alembic` est déjà monté dans le
> conteneur (`Makefile:79`).

## 1.8 Où sont les fichiers

Le répertoire `storage/` du dépôt contient le **contenu initial** du volume permanent. Pour
éviter de le modifier, `make devrun` le recopie (`rsync`) vers `DEVRUN_STORAGE`, par défaut
`./devrun_storage`, et c'est cette copie qui est montée dans le conteneur.

Conséquence pratique : les fichiers produits par l'application — rapports, pièces jointes,
`log/alembic.out` — sont dans `devrun_storage/`, pas dans `storage/`. C'est une source
d'égarement fréquente au début.

Les logs applicatifs, eux, sont montés vers `logs/` à la racine du dépôt. En production ils
se trouvent dans `/var/log/labbook/`. Le détail de chaque log fait l'objet du chapitre
[03](03-storage-et-logs.md).

## 1.9 Récapitulatif

```bash
# prérequis
sudo apt update && sudo apt install -y podman mysql-server make git

# sources
cd $HOME && git clone https://github.com/fondationmerieux/labbook_python.git
cd labbook_python

# configuration
cp doc/labbook.conf.sample $HOME/.config/labbook.conf
$EDITOR $HOME/.config/labbook.conf     # DB_USER, DB_PWD, DB_HOST, ROOTLESS=1

# base de données (dans le client mysql)
#   CREATE USER + GRANT pour 'root'@'10.88.%.%' et 'root'@localhost
#   ALTER USER ... caching_sha2_password ; FLUSH PRIVILEGES
make dbtest && make dbinit

# lancement
make devbuild && make devrun
# → http://localhost:5000/sigl
```
