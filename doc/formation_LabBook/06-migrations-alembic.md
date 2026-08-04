# 06 — Migrations Alembic

## 6.1 Le problème que ça résout

`etc/sql/demo_dump.sql` contient le schéma complet. Il suffit pour une **installation
neuve** — mais personne ne réinstalle à chaque mise à jour.

Un laboratoire en 3.6.20 qui reçoit la 3.6.21 doit obtenir les nouvelles tables, les
nouvelles colonnes et les nouveaux fichiers **sans perdre ses données**. C'est le rôle
d'Alembic : décrire les modifications à appliquer pour passer d'un état au suivant.

Alembic s'exécute **au démarrage du conteneur**, avant le back end
(`labbook_BE/gunicorn.sh:142`), et écrit dans `storage/log/alembic.out`.

## 6.2 Organisation

```
labbook_BE/
├── alembic.ini              configuration ; l'URL de connexion y est adaptée à MySQL
└── alembic/
    ├── versions/            les niveaux de migration (69 à ce jour)
    ├── io/ resource/ upload/    fichiers à copier vers storage/
    └── ...
```

`alembic.ini` construit l'URL `mysql+mysqlconnector://...` à partir des variables
d'environnement, avec repli sur `default_settings.py`. C'est le premier endroit à modifier
si vous vouliez cibler un autre moteur de base.

Les répertoires `io/`, `resource/` et `upload/` reproduisent l'arborescence de `storage/` :
une migration peut avoir besoin d'y déposer un fichier — un nouveau modèle de rapport, par
exemple. Le fichier voyage donc dans les sources d'Alembic.

## 6.3 Un fichier de migration

Nom : `<identifiant>_v3_6_18_increase_size_of_columns.py`. L'identifiant est engendré par
Alembic ; le reste est un commentaire libre, par convention le numéro de version suivi de
l'objet de la migration. Cela permet de retrouver une modification sans ouvrir tous les
fichiers.

Contenu :

```python
revision = '...'            # identifiant de ce niveau
down_revision = '...'       # identifiant du précédent — c'est ce qui fait la chaîne

def upgrade():
    ...

def downgrade():
    pass
```

### Pas de downgrade

`downgrade()` n'est jamais implémenté. On pourrait croire qu'il suffit de retirer une
colonne ajoutée, mais faire reculer un schéma est bien plus délicat que le faire avancer :
les effets de bord sont nombreux et les dégâts difficiles à réparer.

La fonction est laissée avec un `pass` documenté — un `pass` nu est signalé par les outils
d'analyse de code.

> **Conséquence.** Il n'y a pas de retour arrière. Faites une sauvegarde **avant** une mise
> à jour : c'est le seul moyen de revenir en arrière.

### Structure d'un `upgrade()`

```python
def upgrade():
    print(str(datetime.datetime.now()) + ' start migration 3.6.18')

    conn = op.get_bind()

    try:
        conn.execute(text("ALTER TABLE template_setting MODIFY tpl_file VARCHAR(255)"))
    except Exception:
        print("ERROR : cannot modify column tpl_file in template_setting")

    print(str(datetime.datetime.now()) + ' end migration 3.6.18')
```

Quatre conventions :

- **une trace horodatée au début et à la fin**. Un niveau qui s'est bien déroulé produit
  exactement deux lignes dans `alembic.out`, sans rien entre les deux ;
- **`op.get_bind()`** pour obtenir la connexion — c'est la forme imposée par Alembic ;
- **chaque instruction dans son `try / except`**, pour qu'un échec n'interrompe pas les
  suivantes ;
- **un message d'erreur explicite**, indiquant laquelle a échoué. Sur un fichier de dix
  instructions, sans cela, la trace est inexploitable.

Un fichier de migration reste du **Python** : il peut copier des fichiers, tester leur
présence ou leur date. Certains niveaux ne touchent pas du tout à la base et ne font que
livrer un fichier dans `storage/`.

## 6.4 Créer un niveau

Alembic se lance depuis l'environnement virtuel du back end, à l'intérieur du conteneur :

```bash
podman exec -it labbook_python bash
cd /home/apps/labbook_BE/labbook_BE
source venv/bin/activate          # le prompt est préfixé (venv)
alembic revision -m "3.6.21 nouvelle colonne prescripteur"
```

Le fichier est créé dans `alembic/versions/`. Comme ce répertoire est monté, il apparaît
immédiatement dans vos sources — vous l'éditez depuis l'hôte, avec vos outils habituels. On
n'entre dans le conteneur que pour disposer de la commande `alembic`.

Éditez ensuite le fichier engendré :

1. ajouter les imports nécessaires (`datetime`, `sqlalchemy.text`, …) ;
2. remplacer le `pass` de `upgrade()` par les traces et les instructions ;
3. remettre le commentaire habituel dans `downgrade()`.

Puis appliquez :

```bash
make devstop && make devrun
```

> **Note.** `make devbuild` est inutile : `labbook_BE/alembic` est monté dans le conteneur
> (`Makefile:79`). Seul un redémarrage est nécessaire, parce qu'Alembic ne tourne qu'au
> démarrage.

Vérifiez enfin `devrun_storage/log/alembic.out` : deux lignes, `start` et `end`, sans rien
entre elles.

## 6.5 La table `alembic_version`

Alembic mémorise le dernier niveau appliqué dans une table de la base :

```sql
SELECT * FROM alembic_version;
```

Elle contient un identifiant unique, qui doit correspondre au `revision` du dernier fichier
joué.

### Rejouer un niveau

> **Piège — la migration qui ne se rejoue pas.** Votre migration a échoué, vous corrigez le
> fichier, vous redémarrez : il ne se passe rien. Normal — la base se croit déjà au dernier
> niveau et n'y revient pas.
>
> En développement, forcez le retour en arrière :
>
> ```sql
> UPDATE alembic_version SET version_num = '<identifiant du niveau précédent>';
> ```
>
> puis `make devstop && make devrun`.
>
> À réserver au développement. Sur un site en service, un niveau doit avoir été testé avant
> d'être livré.

Corollaire : **modifier un fichier de migration déjà joué chez vous n'a aucun effet chez
vous**, mais en aura chez tous ceux qui n'y sont pas encore parvenus. Corriger un commentaire
est sans risque ; ajouter du code non testé de cette manière est le meilleur moyen de casser
une installation distante.

## 6.6 Conventions du projet

**Un niveau n'est pas créé à chaque version.** Il est créé quand la base ou le contenu de
`storage/` change. La numérotation présente donc des trous : `alembic/versions/` est
l'historique des modifications de schéma, pas celui des versions.

**Plusieurs niveaux pour une même version sont possibles.** Rien n'interdit un `3.6.21` et
un `3.6.21-bis` si le premier devient trop volumineux.

**Le numéro de version applicatif est ailleurs.** Il vit dans les `default_settings.py` du
front end et du back end, et c'est lui qui s'affiche en pied de page. Jouer un niveau Alembic
« 3.6.21 » ne fait pas passer LabBook en 3.6.21 : ce sont deux compteurs indépendants.

**Toujours tester avant de livrer.** Les incidents rencontrés en production sont
généralement liés à une installation personnalisée sur laquelle une modification produisait
un effet non anticipé.

## 6.7 Vérifier un schéma

```sql
DESCRIBE template_setting;   -- structure d'une table
SHOW TABLES;                 -- toutes les tables
```

`DESCRIBE` avant et après un `make devrun` est la façon la plus directe de confirmer qu'une
migration a bien produit son effet.
