# 03 — Le volume `storage` et les logs

## 3.1 Pourquoi un volume séparé

Le conteneur est immuable : tout ce qui y est écrit disparaît à son redémarrage. Or LabBook
doit conserver des comptes rendus, des pièces jointes, des clés et des modèles de documents.

Ces fichiers vivent donc sur un **volume permanent**, extérieur au conteneur et monté
dedans sur `/storage`.

| | Emplacement réel |
|---|---|
| Production | volume permanent créé par l'ISO |
| Développement | `DEVRUN_STORAGE`, par défaut `./devrun_storage` |

Le répertoire `storage/` versionné dans le dépôt contient le **contenu initial** du volume.
`make devrun` le recopie vers `DEVRUN_STORAGE` pour ne pas le modifier.

> **Piège.** Les fichiers produits par l'application sont dans `devrun_storage/`, jamais
> dans `storage/`. Chercher `alembic.out` dans `storage/log/` est une perte de temps
> classique : il est dans `devrun_storage/log/`.

## 3.2 Les répertoires

| Répertoire | Contenu |
|---|---|
| `key/` | secrets générés à la première installation : `secret_key.py` (sessions Flask), `oauth_client_secret.py`, clés GPG de sauvegarde |
| `io/` | entrées/sorties de scripts : sortie de la sauvegarde (`backup.out`), état de synchronisation NTP |
| `log/` | `alembic.out`, et les sorties de scripts qui ne sont pas des logs applicatifs récurrents |
| `report/` | comptes rendus générés. Vide sur une installation neuve. |
| `resource/` | ressources livrées par défaut : logo, feuilles de calcul DHIS2, configuration des rapports épidémiologiques et d'indicateurs, et `resource/template/` pour les modèles de documents |
| `upload/` | pièces jointes déposées par les utilisateurs |

Les trois derniers sont ceux à ne surtout pas perdre : la sauvegarde couvre la base **et**
le volume de stockage, précisément pour eux.

### Le cas de `upload/`

Deux dossiers différents peuvent recevoir une pièce jointe portant le même nom. Pour éviter
qu'elles s'écrasent, chaque fichier déposé est **renommé par une empreinte**, et rangé dans
une arborescence construite sur ses deux premiers caractères.

Le nom d'origine est conservé en base ; il est restitué à l'utilisateur au téléchargement.
Conséquence : les fichiers de `upload/` sont illisibles depuis le système de fichiers, et
c'est voulu.

### `resource/template/`

Les modèles de comptes rendus, au format ODT. On y trouve notamment des variantes `RTL`
(*right to left*) pour les langues écrites de droite à gauche, comme l'arabe. Les modèles
ajoutés par un laboratoire atterrissent ici également.

> **Note.** Sur une installation issue de l'ISO, `storage/` contient des répertoires
> supplémentaires (`audit/`, ressources de Connect) créés par l'ISO et absents en mode
> développement. Le code crée les répertoires manquants avec `mkdir -p` avant d'écrire,
> plutôt que d'échouer.

## 3.3 Les logs

Les logs applicatifs sont écrits dans `/home/apps/logs/` à l'intérieur du conteneur, et
montés vers `logs/` à la racine du dépôt en développement, `/var/log/labbook/python/` en
production.

Ils sont donc consultables **sans entrer dans le conteneur** — utile quand vous demandez
des logs à un exploitant qui ne connaît pas podman.

### Lequel lire

| Log | Contenu | Quand le lire |
|---|---|---|
| `log_db.log` | requêtes SQL et erreurs de base | **le plus important**. Toute erreur SQL, de syntaxe ou de colonne, est ici. |
| `log_services.log` | entrées de l'API back end | pour savoir quel service a été appelé et avec quoi |
| `log_front.log` | traces serveur du front end | rendu de page, changement de langue, connexion |
| `gunicorn-BE-error.log` | exceptions non rattrapées du back end | erreurs HTTP 500 |
| `gunicorn-FE-error.log` | exceptions non rattrapées du front end | plus rare : le front end casse moins souvent |
| `gunicorn-BE-access.log` / `-FE-access.log` | journal d'accès, façon Apache | analyse de charge |
| `log_wsgi.log` | couche proxy | problèmes de routage ou de préfixe d'URL |
| `gunicorn.out` | sortie de lancement de gunicorn | quasiment toujours vide |
| `log_script.log`, `log_script_analyzer.log` | scripts shell et échanges automates | chapitre [09](09-exploitation.md) |
| `scheduler.out` | tâches planifiées | chapitre [09](09-exploitation.md) |

Et, hors de ce répertoire, dans le stockage : `storage/log/alembic.out`, le journal des
migrations (chapitre [06](06-migrations-alembic.md)).

### Format

Tous les logs applicatifs partagent le même format, produit par `Logs.fileline()`
(`labbook_BE/app/models/Logs.py`) : horodatage, chemin du fichier, fonction, numéro de
ligne, message.

```
2026-07-22 11:59:03 /home/apps/.../models/Dict.py:insertEvent:412 : TRACE insert event
```

C'est pourquoi le code est parsemé de `log.info(Logs.fileline() + ' : ...')` plutôt que de
s'appuyer sur les informations d'appel natives de `logging`.

### Journaliser une valeur venue de l'utilisateur

Une valeur saisie par l'utilisateur ne part jamais telle quelle dans le journal : elle passe
d'abord par `Logs.clean()`, qui remplace les retours à la ligne et les tabulations par des
espaces.

```python
log.info(Logs.fileline() + ' : TRACE search doctor=' + Logs.clean(name))
```

Sans cela, une valeur contenant un retour à la ligne écrit **plusieurs lignes** dans le
fichier, dont une qui imite le format ci-dessus. Le journal devient alors une source dans
laquelle on ne peut plus avoir confiance, et les recherches d'erreur portent à faux.

### Erreur rattrapée ou non

Distinction utile au débogage :

- **rattrapée** (`try / except` dans le code) → un message propre dans `log_db.log` ou
  `log_services.log` ;
- **non rattrapée** → une trace d'une vingtaine de lignes dans `gunicorn-BE-error.log`.
  Seules les dernières lignes comptent : elles donnent le fichier, la fonction et la ligne.

### Rotation

Rotation **hebdomadaire** avec compression, pilotée par `logrotate.d/` et le service
supervisor `logrotate_labbook`. `alembic.out` a sa propre règle (180 archives conservées).

> **Piège — l'erreur d'il y a trois semaines.** Le log courant ne contient que la semaine
> écoulée. Si un utilisateur signale une erreur ancienne, demandez-lui l'archive
> correspondante, pas le fichier courant. Et demandez-lui surtout **la date, l'heure et
> l'action** : une semaine de log représente des dizaines de milliers de lignes.

LabBook ne fait aucun ménage au-delà de la rotation, et ne surveille pas l'espace disque.
Sur un serveur en service depuis des années, c'est à l'administrateur de s'en occuper.
