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

List backup servers:

```
kdna server list <project_name>
```

### Example

```
kdna server list <project_name>
```

#### Options

| Options |  Type  |   Description    | Required |
|:--------|:------:|:----------------:|:--------:|
|         | String |   project_name   |   True   |

---

---

## Auto-Backup

---

### Description

Manage regular backups

```
kdna auto-backup <command> [options] [arguments]
```

---

### Creation

#### Use

Create a regular backup 

```
kdna auto-backup create -i <id_backup> -n <backup_name> -t <tag> <cron_schedule> <custom_schedule> -d <start_date> -s <id_server> -p <path_file/file_backup>
``` 

#### Example

```
kdna auto-backup create -i 1 -n backup -t tag -d 2021-01-01 -s 1 -p /home
```

#### Options

| Options |  Type  |   Description   | Required |
|:--------|:------:|:---------------:|:--------:|
| -i      | String |    id_backup    |   True   |
| -n      | String |   backup_name   |   True   |
| -t      | String |       tag       |   True   |
|         | String |  cron_schedule  |   True   |
|         | String | custom_schedule |   False  |
| -d      | String |   start_date    |   True   |
| -s      | String |    id_server    |   True   |
| -p      | String |   path_backup   |   True   |

---

### Delete

#### Use

Delete a regular backup

```
kdna auto-backup delete -i <id_backup>
```

#### Example

```
kdna auto-backup delete -i 1
```

#### Options

| Options |  Type  | Description | Required |
|:--------|:------:|:-----------:|:--------:|
| -i      | String |  id_server  |   True   |

---

### Update

#### Use

Update a regular backup
```
kdna auto-backup update -i <id_backup> -t <tag> <tag_updated> cron_schedule <<custom_schedule>> -d <start_date> -p <path_backup>
```

#### Example

```
kdna auto-backup update -i 1 -d 2021-01-01 -p /home
```

#### Options

| Options |  Type  |     Description      | Required |
|:--------|:------:|:--------------------:|:--------:|
| -i      | String |      id_backup       |   True   |
| -t      | String | tag & tag updated    |   False  |
|         | String |    cron_schedule     |   False  |
|         | String |   custom_schedule    |   False  |
| -d      | String |      start_date      |   False  |
| -p      | String |     path_backup      |   False  |

Please note: you cannot change the server id, as the backup is linked to it.
---

### List

#### Use

List regular backups
```
kdna auto-backup list
```

---

## Backup

---

### Description

Managing manual backups

```
kdna backup <command> [options] [arguments]
```

---

### Creation

Create a backup

#### Use

```
kdna backup add <name:tag_backup> <path_backup>
``` 

#### Example

```
kdna backup add backup:tag /home
```

#### Options

| Options |  Type  | Description | Required |
|:--------|:------:|:-----------:|:--------:|
|         | String | name:tag_backup  |   True   |
|         | String | path_backup |   True   |

---

### Delete

#### Use

Delete a backup

```
kdna backup delete -t <path:tag>
```

#### Example

```
kdna backup delete -t /home:tag
```

#### Options

| Options |  Type  | Description | Required |
|:--------|:------:|:-----------:|:--------:|
| -t      | String |  path:tag   |   True   |

---

### Restore

#### Use

Restore a backup
```
kdna backup restore -t <name:tag> <path_backup>
```

Example

```
kdna backup restore -t backup:tag /home
```

#### Options

| Options |  Type  | Description | Required |
|:--------|:------:|:-----------:|:--------:|
| -t      | String |  name:tag   |   True   |
|         | String | path_backup |   False   |

---

### List

#### Use

List backups

```
kdna backup list
```

---

## Encrypt

---

### Description

Backup encryption management

```
kdna encrypt <command> [options]
```

---

### Generate

Generate an encryption key

#### Use

```
kdna encrypt keygen <path>
``` 

#### Example

```
kdna encrypt keygen /home
```

#### Options

| Options |  Type  | Description | Required |
|:--------|:------:|:-----------:|:--------:|
|         | String |    path     |   True   |

---

### Activation

#### Use

Activate encryption

```
kdna encrypt activate
```


---

### Désactivation

#### Use

Desactivate encryption
```
kdna encrypt deactivate
```

---

## Tag

---

### Description

Manage tags 

```
kdna tag <command> [options]
```

---

### Creation

Create a tag

#### Use

```
kdna tag add -t <tag> -p <project> -f <file>
``` 

#### Example

```
kdna tag -t tag -p project_name -f a_file
```

#### Options

| Options |  Type  | Description | Required |
|:--------|:------:|:-----------:|:--------:|
| -t      | String |     tag     |   True   |
| -p      | String |   project   |   True   |
| -f      | String |    file     |   True   |


---

### List

#### Use

List tags

```
kdna tag list
```


---
