# 05 — Traductions

LabBook est traduit dans neuf langues. Deux mécanismes coexistent, et les confondre est la
source d'erreur la plus fréquente sur ce sujet.

| | Concerne | Où c'est stocké |
|---|---|---|
| **Catalogues Babel** | le texte de l'interface | fichiers `.po` / `.mo` du dépôt |
| **Table `translation`** | le référentiel métier (analyses, dictionnaires, variables) | base de données |

Les deux se pilotent différemment, et n'ont ni le même cycle de vie ni la même couverture
linguistique.

## 5.1 Les langues

`fr_FR` (défaut), `en_GB`, `en_US`, `es`, `pt`, `ar`, `km`, `lo`, `mg`.

`en_GB` et `en_US` partagent les mêmes traductions : seul le format de date les distingue.

Le français est la langue de référence de l'interface. À l'inverse, la documentation et les
commentaires de code sont en anglais.

> **Attention à une confusion courante.** Les catalogues Babel du back end existent pour les
> neuf langues, comme ceux du front end. C'est le **référentiel stocké en base** qui est
> limité à trois langues (français, anglais, portugais) : traduire des noms d'analyses exige
> un vocabulaire métier qui n'est pas disponible partout. Dire que « le back end n'a que
> trois langues » est donc inexact — la limite porte sur la table `translation`, pas sur les
> catalogues.

L'utilisateur dispose de deux réglages distincts : le sélecteur de langue de l'interface, et
dans *Préférences*, la langue des rapports et celle du référentiel.

## 5.2 Catalogues Babel

### Marquer une chaîne

Dans un template :

```jinja
{{ _("Rapport d'activité") }}
```

Dans du Python :

```python
_("Rapport d'activité")
```

La chaîne française sert directement de **clé**. C'est un choix : une clé abstraite du type
`report.activity.title` serait plus rigoureuse, mais si la traduction manque, l'utilisateur
verrait `report.activity.title` à l'écran. Avec la convention retenue, il voit le texte
français — dégradé, mais compréhensible.

### Ce qui est extrait

Défini par `babel.cfg`, différent dans chaque application :

| Application | Sources extraites |
|---|---|
| Front end | `**.py`, `models/**.py`, `templates/**.html`, `templates/**.js` |
| Back end | `**.py`, `models/**.py`, `services/Pdf.py`, `translations/**.py` |

### Les fichiers

```
app/translations/
├── messages.pot            toutes les clés, commun à toutes les langues
├── messages_pybabel.py     (voir 5.4)
├── fr_FR/LC_MESSAGES/
│   ├── messages.po         clés + traductions, éditable
│   └── messages.mo         version compilée, binaire
├── en_GB/...
└── ...
```

Le `.po` indique, pour chaque clé, les fichiers où elle apparaît. Le `.mo` est le fichier
réellement utilisé à l'exécution.

### Le cycle en trois commandes

Depuis l'environnement virtuel de l'application concernée :

```bash
pybabel extract -F babel.cfg -o translations/messages.pot .   # 1. collecter les clés
pybabel update -i translations/messages.pot -d translations/  # 2. répercuter dans chaque .po
pybabel compile -d translations/                              # 3. produire les .mo
```

`extract` ajoute les clés nouvelles et retire celles qui ne sont plus utilisées ; `update`
met à jour les `.po` de chaque langue ; `compile` produit les `.mo`.

> **Piège — l'option `--no-fuzzy-matching`.** Sans elle, `pybabel update` recopie la
> traduction d'une clé ressemblante dans une clé voisine, en la marquant `fuzzy`. Sur des
> libellés proches (« ascenseur montant » / « ascenseur descendant »), on récolte des
> traductions fausses, très difficiles à repérer ensuite. Mieux vaut une case vide qu'une
> traduction inventée.

### Ajouter une langue

```bash
pybabel init -i translations/messages.pot -d translations/ -l <locale>
```

Le répertoire est créé, puis `update` et `compile` comme d'habitude.

### Modifier une traduction existante

1. éditer la ligne dans le `.po` de la langue ;
2. `pybabel compile` ;
3. vérifier que le `.mo` est bien à sa place.

> **Piège — le cache.** Il arrive, rarement, qu'une traduction corrigée ne s'affiche pas
> malgré les trois étapes. C'est une mise en cache : arrêter et relancer le conteneur la
> vide.

### Traduction collaborative

Le format `.po` est standard. Le projet passe par **poeditor.com** : on y envoie le `.pot`,
un traducteur remplit les cases dans une interface web, on récupère les `.po`. Un éditeur de
texte fonctionne tout aussi bien pour quelques chaînes.

## 5.3 Ce qui se passe quand une clé manque

Utile à connaître, parce que c'est le symptôme habituel :

- vous modifiez un libellé dans un template ;
- vous rafraîchissez : le nouveau texte s'affiche en français ;
- vous basculez en anglais : **toute la page passe en anglais, sauf ce libellé**.

Rien d'anormal. La nouvelle chaîne n'est pas encore une clé connue : Babel ne la trouve pas
dans le catalogue et affiche la clé, c'est-à-dire le texte français. Il faut refaire
`extract`, `update`, `compile`.

## 5.4 `messages_pybabel.py`

Fichier présent dans les deux applications. **Ce n'est pas du code exécutable** : c'est une
liste de chaînes enveloppées dans `_("...")`.

Il existe parce que `pybabel` ne sait extraire que depuis des fichiers source. Or certaines
chaînes à traduire viennent de la base : libellés de dictionnaires, familles d'analyses,
noms de variables. Les recopier ici les rend visibles à l'extraction — `babel.cfg` du back
end déclare explicitement `translations/**.py` comme source.

Quand une nouvelle analyse ou un nouveau libellé de dictionnaire doit être traduisible, sa
chaîne est ajoutée à ce fichier.

## 5.5 Le référentiel en base

Les noms d'analyses, de dictionnaires et de variables sont stockés dans les tables métier,
en français. Leurs traductions vivent dans une table dédiée, `translation`, dont les
colonnes principales sont :

| Colonne | Rôle |
|---|---|
| `tra_type` | catégorie : nom d'analyse, libellé de dictionnaire, nom de dictionnaire, nom de variable |
| `tra_ref` | identifiant de la ligne traduite dans sa table d'origine |
| la langue et le texte traduit | |

Cette table sert notamment les **champs de recherche** : chercher une analyse par son nom
fait une jointure sur `translation` plutôt qu'un balayage des tables métier.

### Comment elle est alimentée

Pas directement par Alembic : traduire suppose que Babel soit chargé, ce qui n'est pas le
cas au moment où Alembic s'exécute. Le mécanisme se fait donc en deux temps :

1. le niveau Alembic insère une ligne dans la table `init_version`, qui signale un travail à
   faire ;
2. au démarrage, le back end voit cette ligne, effectue la mise à jour des traductions, et
   inscrit le résultat.

Conséquence : **les traductions du référentiel ne changent qu'à l'occasion d'une nouvelle
version**.

### Limite connue

> **Piège — le référentiel désynchronisé.** Renommer une analyse depuis l'interface met à
> jour la table des analyses, **mais pas la table `translation`**. La recherche par nom
> passant par `translation`, l'analyse renommée devient introuvable par son nouveau nom.
> Elle reste trouvable par son code.
>
> Il n'existe aujourd'hui aucune synchronisation automatique. Le contournement est de
> corriger la ligne correspondante de `translation` en SQL. Rendre les deux cohérentes
> serait une évolution du logiciel, pas une simple correction.

### Trouver la ligne à corriger

```sql
-- catégories disponibles
SELECT tra_type, COUNT(*) FROM translation GROUP BY tra_type;

-- l'analyse concernée, pour récupérer son identifiant
SELECT id_data, ... FROM sigl_05_data WHERE ...;

-- sa traduction
SELECT * FROM translation WHERE tra_ref = <id_data> AND tra_type = <type>;
```

Les tables du référentiel sont décrites au chapitre [07](07-back-end.md) et dans
`doc/tables.md`.
