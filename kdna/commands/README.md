# Commandes

## Aide

Obtenir les informations nécessaires à l'utilisation de chaque commande

```
kdna <commande> --help
kdna <commande> <sous-commande> --help
```

## Server

---

### Description

Gérer un serveur pour les backups

```
kdna server <commande> <sous-commande> [options] [arguments]
```

---

### Sélection

#### Usage

```
kdna server set -i <id_serveur> -a <alias_serveur> -c <credentials> -p <port_serveur>
```

#### Exemple

```
kdna server set -i 1 -a alias -c test_credentials -p 22
```

#### Options

| Options |  Type  | Description | Required |
|:--------|:------:|:-----------:|:--------:|
| -i      | String |  id_server  |   Vrai   |
| -a      | String |    alias    |   Vrai   |
| -c      | String | credentials |   Vrai   |
| -p      | String |    port     |   Vrai   |

---

### Suppression de la sélection d'un serveur

#### Usage

```
kdna server delete -a <alias_serveur> -i <id_serveur>
```

#### Exemple

```
kdna server delete -i 1
```

#### Options

| Options |  Type  | Description | Required |
|:--------|:------:|:-----------:|:--------:|
| -i      | String |  id_server  |   Faux   |
| -a      | String |    alias    |   Faux   |

A noter : Une seule des deux options doit être impérativement choisie

---

### Update

#### Usage

```
kdna server update <alias_serveur> -c <new_credentials> -p <new_port_serveur> -a <new_alias>
```

#### Exemple

```
kdna server update alias_serveur -c new_credentials
```

#### Options

| Options |  Type  |   Description    | Required |
|:--------|:------:|:----------------:|:--------:|
|         | String |      alias       |   Vrai   |
| -c      | String | new_credentials  |   Faux   |
| -p      | String | new_port_serveur |   Faux   |
| -a      | String |    new_alias     |   Faux   |

---

### List

#### Usage

```
kdna server list
```

---

## Auto-Backup

---

### Description

Gérer des backups régulières

```
kdna auto-backup <commande> <sous-commande> [options] [arguments]
```

---

### Création

#### Usage

```
kdna auto-backup schedule -i <id_backup> -n <nom_backup> -t <tag> <cron_schedule> <custom_schedule> -d <date_debut> -s <id_server> -p <path_fichier/dossier_backup>
``` 

#### Exemple

```
kdna auto-backup schedule -i 1 -n backup -t tag -d 2021-01-01 -s 1 -p /home
```

#### Options

| Options |  Type  |   Description   |                     Required                     |
|:--------|:------:|:---------------:|:------------------------------------------------:|
| -i      | String |    id_backup    |                       Vrai                       |
| -n      | String |   nom_backup    |                       Vrai                       |
| -t      | String |       tag       |                       Vrai                       |
|         | String |  cron_schedule  |                       Vrai                       |
|         | String | custom_schedule | Faux, Vrai si le cron_schedule choisi est custom |
| -d      | String |   date_debut    |                       Vrai                       |
| -s      | String |    id_server    |                       Vrai                       |
| -p      | String |   path_backup   |                       Vrai                       |

---

### Suppression

#### Usage

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

```
kdna auto-backup update -i <id_backup> cron_schedule <<custom_schedule>> -d <date_debut> -p <path_backup>
```

#### Exemple

```
kdna auto-backup update -i 1 -d 2021-01-01 -p /home
```

#### Options

| Options |  Type  |   Description   |                  Required                  |
|:--------|:------:|:---------------:|:------------------------------------------:|
| -i      | String |    id_backup    |                    Vrai                    |
|         | String |  cron_schedule  |                    Faux                    |
|         | String | custom_schedule | Faux (vrai si le cron_schedule est custom) |
| -d      | String |   date_debut    |                    Faux                    |
| -p      | String |   path_backup   |                    Faux                    |

A noter: on ne peut pas modifier l'id du serveur car la backup est liée à celui-ci

---

### List

#### Usage

```
kdna auto-backup list
```

---

## Backup

---

### Description

Gérer des backups manuelles

```
kdna backup <commande> <sous-commande> [options] [arguments]
```

---

### Création

#### Usage

```
kdna backup add <nom_backup> <path_backup>
``` 

#### Exemple

```
kdna backup add backup /home
```

#### Options

| Options |  Type  | Description | Required |
|:--------|:------:|:-----------:|:--------:|
|         | String | nom_backup  |   Vrai   |
|         | String | path_backup |   Vrai   |

---

### Suppression

#### Usage

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

```
kdna backup list
```
