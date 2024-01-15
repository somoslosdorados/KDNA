# Commands

## Help

Get the information you need to use each command
```
kdna <command> --help
kdna <command> <subcommand> --help
```

## Server

---

### Description

Managing a backup server

```
kdna server <command> [options] [arguments]
```

---

### Add

#### Use

Adding a backup server
```
kdna server add -i <id_server> -ad <libele_connexion> -a <alias_server> -r <repo_backup> -p <port_server>
```

#### Example

```
kdna server add -i S1 -ad kdna@162.38.112.110 -a alias -r /my/repository/backup/ -p 22
```

#### 

#### Options

| Options |  Type  |        Description         | Required |
|:--------|:------:|:--------------------------:|:--------:|
| -i      | String |         id_server          |   Vrai   |
| -ad     | String |    libellé de connexion     |   Vrai   |
| -a      | String |           alias            |   Vrai   |
| -r      | String | répertoire pour les backup |   Vrai   |
| -p      | String |            port            |   Vrai   |
| -e      | Boolean |         encrypt           |   False   |
---

### Deleting a backup server

#### Use

Remove a backup server

```
kdna server delete -a <alias_server> -i <id_server>
```

#### Example

```
kdna server delete -i 1
```

#### Options

| Options |  Type  | Description | Required |
|:--------|:------:|:-----------:|:--------:|
| -i      | String |  id_server  |   False  |
| -a      | String |    alias    |   False  |

Please note: Only one of the two options must be chosen.

---

### Update

#### Use

Updating a server
```
kdna server update <alias_server> -c <new_credentials> -p <new_port_server> -ad <new_address> -a <new_alias>
```

#### Example

```
kdna server update alias_server -c new_credentials
```

#### Options

| Options |  Type  |   Description    | Required |
|:--------|:------:|:----------------:|:--------:|
|         | String |      alias       |   True   |
| -c      | String | new_credentials  |   False  |
| -p      | String | new_port_serveur |   False  |
| -ad     | String |   new_address    |   False  |
| -a      | String |    new_alias     |   False  |

---

### List

#### Use

Lister les serveurs de backup

```
kdna server list <project_name>
```

### Exemple

```
kdna server list project_name
```

#### Options

| Options |  Type  |   Description    | Required |
|:--------|:------:|:----------------:|:--------:|
|         | String |   project_name   |   Vrai   |

---

---

## Auto-Backup

---

### Description

Gérer des backups régulières

```
kdna auto-backup <commande> [options] [arguments]
```

---

### Création

#### Usage

Créer une backup régulière

```
kdna auto-backup create -i <id_backup> -n <nom_backup> -t <tag> <cron_schedule> <custom_schedule> -d <date_debut> -s <id_server> -p <path_fichier/dossier_backup>
``` 

#### Exemple

```
kdna auto-backup create -i 1 -n backup -t tag -d 2021-01-01 -s 1 -p /home
```

#### Options

| Options |  Type  |   Description   | Required |
|:--------|:------:|:---------------:|:--------:|
| -i      | String |    id_backup    |   Vrai   |
| -n      | String |   nom_backup    |   Vrai   |
| -t      | String |       tag       |   Vrai   |
|         | String |  cron_schedule  |   Vrai   |
|         | String | custom_schedule |   Faux   |
| -d      | String |   date_debut    |   Vrai   |
| -s      | String |    id_server    |   Vrai   |
| -p      | String |   path_backup   |   Vrai   |

---

### Suppression

#### Usage

Supprimer une backup régulière

```
kdna auto-backup delete -i <id_backup>
```

#### Exemple

```
kdna auto-backup delete -i 1
```

#### Options

| Options |  Type  | Description | Required |
|:--------|:------:|:-----------:|:--------:|
| -i      | String |  id_server  |   Vrai   |

---

### Update

#### Usage

Mettre à jour une backup régulière

```
kdna auto-backup update -i <id_backup> -t <tag> <tag_updated> cron_schedule <<custom_schedule>> -d <date_debut> -p <path_backup>
```

#### Exemple

```
kdna auto-backup update -i 1 -d 2021-01-01 -p /home
```

#### Options

| Options |  Type  |     Description      | Required |
|:--------|:------:|:--------------------:|:--------:|
| -i      | String |      id_backup       |   Vrai   |
| -t      | String | tag & tag mis à jour |   Faux   |
|         | String |    cron_schedule     |   Faux   |
|         | String |   custom_schedule    |   Faux   |
| -d      | String |      date_debut      |   Faux   |
| -p      | String |     path_backup      |   Faux   |

A noter: on ne peut pas modifier l'id du serveur car la backup est liée à celui-ci

---

### List

#### Usage

Lister les backups régulières

```
kdna auto-backup list
```

---

## Backup

---

### Description

Gérer des backups manuelles

```
kdna backup <commande> [options] [arguments]
```

---

### Création

Créer une backup

#### Usage

```
kdna backup add <nom:tag_backup> <path_backup>
``` 

#### Exemple

```
kdna backup add backup:tag /home
```

#### Options

| Options |  Type  | Description | Required |
|:--------|:------:|:-----------:|:--------:|
|         | String | nom:tag_backup  |   Vrai   |
|         | String | path_backup |   Vrai   |

---

### Suppression

#### Usage

Supprimer une backup

```
kdna backup delete -t <path:tag>
```

#### Exemple

```
kdna backup delete -t /home:tag
```

#### Options

| Options |  Type  | Description | Required |
|:--------|:------:|:-----------:|:--------:|
| -t      | String |  path:tag   |   Vrai   |

---

### Restore

#### Usage

Restaurer une backup

```
kdna backup restore -t <name:tag> <path_backup>
```

Exemple

```
kdna backup restore -t backup:tag /home
```

#### Options

| Options |  Type  | Description | Required |
|:--------|:------:|:-----------:|:--------:|
| -t      | String |  name:tag   |   Vrai   |
|         | String | path_backup |   Faux   |

---

### List

#### Usage

Lister les backups

```
kdna backup list
```

---

## Encrypt

---

### Description

Gérer l'encryption des backups

```
kdna encrypt <commande> [options]
```

---

### Génération

Générer une clé de cryptage

#### Usage

```
kdna encrypt keygen <path>
``` 

#### Exemple

```
kdna encrypt keygen /home
```

#### Options

| Options |  Type  | Description | Required |
|:--------|:------:|:-----------:|:--------:|
|         | String |    path     |   Vrai   |

---

### Activation

#### Usage

Activer l'encryption

```
kdna encrypt activate
```


---

### Désactivation

#### Usage

Désactiver l'encryption

```
kdna encrypt deactivate
```

---

## Tag

---

### Description

Gérer les tags

```
kdna tag <commande> [options]
```

---

### Création

Créer un tag 

#### Usage

```
kdna tag add -t <tag> -p <project> -f <file>
``` 

#### Exemple

```
kdna tag -t tag -p un_projet -f a_file
```

#### Options

| Options |  Type  | Description | Required |
|:--------|:------:|:-----------:|:--------:|
| -t      | String |     tag     |   Vrai   |
| -p      | String |   project   |   Vrai   |
| -f      | String |    file     |   Vrai   |


---

### List

#### Usage

Lister les tags

```
kdna tag list
```


---
