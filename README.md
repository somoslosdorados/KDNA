# KDNA

This is the official repository for the DO2023-2026 python CLI backup project

## Documentation

After cloning the repo you will need to install all dependencies

```bash
Utils.initialize_config_file()
```

Un fichier est créé :

```
[servers]

[auto-backups]

```

Vous pouvez désormais faire vos commandes dans le fichier `__init__.py`


### Aide
Obtenir les informations nécessaires à l'utilisation de chaque commande
```
# kdna <commande> --help
# kdna <commande> <sous-commande> --help
```

### Server

---

#### Description
Gérer un serveur pour les backups
```
kdna server <commande> <sous-commande> [options] [arguments]
```
---

1. #### Création

#### Usage
```
kdna server set -i <id_serveur> -a <alias_serveur> -c <credentials> -p <port_serveur>
```
Exemple

```
kdna server set -i 1 -a alias -c test_credentials -p 22
```

#### Options
| Options |  Type  | Description | Required |
| :------ |:------:| :---------: |:--------:|
| -i      | String |   id_server |   Vrai   |
| -a      | String |   alias     |   Vrai   |
| -c      | String |   credentials |   Vrai   |
| -p      | String |   port      |   Vrai   |


2. #### Suppression

#### Usage
```
kdna server delete -a <alias_serveur> -i <id_serveur>
```
Exemple

```
kdna server delete -i 1
```

#### Options
| Options |  Type  | Description | Required |
| :------ |:------:| :---------: |:--------:|
| -i      | String |   id_server |   Faux   |
| -a      | String |   alias     |   Faux   |

A noter : au moins une des deux options doit être choisie

3. #### Update

#### Usage
```
kdna server update -a <alias_serveur> -c <credentials> -p <port_serveur> -a <new_alias>
```
Exemple

```
kdna server update alias_serveur -c new_credentials
```

#### Options
| Options |  Type  | Description | Required |
|:--------|:------:| :---------: |:--------:|
|         | String |   alias     |   Vrai   |
| -c      | String |   credentials |   Faux   |
| -p      | String |   port      |   Faux   |
| -a      | String |   new_alias |   Faux   |

3. #### List

#### Usage
```
kdna server list
```

### Auto-Backup

---

#### Description
Gérer des backups régulières
```
kdna auto-backup <commande> <sous-commande> [options] [arguments]
```
---

1. #### Création

#### Usage
```
kdna auto-backup schedule -i <id_backup> -n <nom_backup> -t <tag> cron_schedule <<custom_schedule>> -d <date_debut> -s <id_server> -p <path_backup>
``` 

Exemple

```
kdna auto-backup schedule -i 1 -n backup -t tag -d 2021-01-01 -s 1 -p /home
```

#### Options
| Options |  Type  | Description | Required |
| :------ |:------:| :---------: |:--------:|
| -i      | String |   id_backup |   Vrai   |
| -n      | String |   nom_backup|   Vrai   |
| -t      | String |   tag       |   Vrai   |
|         | String |cron_schedule|   Vrai   |
|         | String |custom_schedule|   Faux   |
| -d      | String |   date_debut|   Vrai   |
| -s      | String |   id_server |   Vrai   |
| -p      | String |   path_backup|   Vrai   |


2. #### Suppression

#### Usage
```
kdna auto-backup delete -i <id_backup>
```
Exemple

```
kdna auto-backup delete -i 1
```

#### Options
| Options |  Type  | Description | Required |
| :------ |:------:| :---------: |:--------:|
| -i      | String |   id_server |   Vrai   |

3. #### Update

#### Usage
```
kdna auto-backup update -i <id_backup> cron_schedule <<custom_schedule>> -d <date_debut> -p <path_backup>
```
Exemple

```
kdna auto-backup update -i 1 -d 2021-01-01 -p /home
```

#### Options
| Options |  Type  | Description |                  Required                  |
|:--------|:------:| :---------: |:------------------------------------------:|
| -i      | String |   id_backup |                    Vrai                    |
|         | String |cron_schedule|                    Faux                    |
|         | String |custom_schedule| Faux (vrai si le cron_schedule est custom) |
| -d      | String |   date_debut|                    Faux                    |
| -p      | String |   path_backup|                    Faux                    |

A noter: on ne peut pas modifier l'id du serveur car la backup est liée à celui-ci

3. #### List

#### Usage
```
kdna auto-backup list
```

### Backup

---

#### Description
Gérer des backups manuelles
```
kdna backup <commande> <sous-commande> [options] [arguments]
```
---

1. #### Création

#### Usage
```
kdna backup add <nom_backup> <path_backup>
``` 

Exemple

```
kdna backup add backup /home
```

#### Options
| Options |  Type  | Description | Required |
|:--------|:------:| :---------: |:--------:|
|         | String |   nom_backup|   Vrai   |
|       | String |   path_backup|   Vrai   |


2. #### Suppression

#### Usage
```
kdna backup delete -t <path:tag>
```
Exemple

```
kdna backup delete -t /home:tag
```

#### Options
| Options |  Type  | Description | Required |
| :------ |:------:| :---------: |:--------:|
| -t      | String |   path:tag  |   Vrai   |

3. #### Restore

#### Usage
```
kdna backup restore -t <name:tag> <path_backup>
```
Exemple

```
kdna backup restore -t backup:tag /home
```

#### Options
| Options |  Type  | Description |                  Required                  |
|:--------|:------:| :---------: |:------------------------------------------:|
| -t      | String |   name:tag  |                    Vrai                    |
|         | String |   path_backup|                    Faux                    |

4. #### List

#### Usage
```
kdna backup list
```


---

### Utils

1. #### Readall

Vous pouvez faire la commande suivante pour vous afficher le contenu du fichier  `config.txt` simplement :

```
Utils.read_all()

### Start the app
```bash
poetry run python KDNA/__init__.py
```
### Run the tests
```bash
poetry run pytest
```
### Run the pipeline
```bash
poetry run tox run-parallel
```
```bash
#run the pipeline with a specific env
poetry run tox run-parallel -e (env)
```
### Build the documentation
```bash
sphinx-apidoc -f -o docs/source kdna/
sphinx-build -M html docs/source/ docs/build/
```

Cette méthode n'est pas poussée car un POC est destiné à la lecture d'un fichier de conf (cf. POC 2)

## TODO :

-   générer un id aléatoire
-   revoir les timestamp des auto-backups
-   revoir les frequency des auto-backups
-   optimiser au maximum le code

## Package added
    - click             # Parseur
    - fabric            # SSH client
    - pycryptodome      # Encrypt tool
    - pylint            # Linter
    - mypy              # Type checker
    - pytest            # Test framework
    - tox               # Test runner
    - tox-gh-actions    # Tox github action
    - sphinx            # Documentation generator
    - sphinx-rtd-theme  # Read the docs theme
    - sphinx-autoapi    # Auto documentation generator
    - m2r2              # Markdown to reStructuredText converter
    - pydocstyle        # Docstring style checker
    - chardet           # Encoding detector

## POC-Parsing

Ce POC permet de récupérer un document au format .conf et de le parser afin de récupérer les caractéristiques des serveurs et des auto-backups qui y sont inscrites.
La lecture du fichier de configuration va faire appel à des stratégies différentes en fonction des headers ("[...]") lu et affecter les informations à des instances de classe.

Pour ce POC j'ai travaillé en grande majorité seule (85%), au début et à la fin du projet j'ai pu discuter avec Tristan et Giada pour trouver une bonne façon d'appliquer des stratégies différenciées.

