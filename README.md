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

### Server

1. #### Création

Vous pouvez créer un serveur avec ces différents paramètres :

| Signature : | id_server | credentials |  port  |  alias |
| :---------- | :-------: | :---------: | :----: | -----: |
| Type :      |  String   |   String    | String | String |

Comme ceci :

```
server = Server("18", "credentials", "22", "hello")
```

2. #### Suppression

Vous pouvez supprimer un serveur avec ces différents paramètres :

| Signature : |  id_server  |   by_alias |
| :---------- | :---------: | ---------: |
| Type :      |   String    |    Boolean |
| Règle :     | Obligatoire | Facultatif |

Vous pouvez supprimer un serveur grâce à son id de cette manière :

```
Server.delete("18")
```

Mais vous pouvez aussi supprimer un serveur grâce à son alias de cette manière :

```
Server.delete("hello", by_alias=True)
```

À noter que l'attribut `by_alias` possède de base la valeur `False` c'est pourquoi vous n'avez pas besoin de le préciser lorsque vous voulez effectuer une suppresion par id.

3. #### Update

Vous pouvez mettre à jour un serveur grâce à son alias avec ces différents paramètres :

| Signature : |    alias    | credentials |    port    | nouvel alias |
| :---------- | :---------: | :---------: | :--------: | -----------: |
| Type :      |   String    |   String    |   String   |       String |
| Règle :     | Obligatoire | Facultatif  | Facultatif |   Facultatif |

```
Server.update("test", new_port="25", new_credentials="test", new_alias="ahahah")
```

À noter que vous n'êtes pas obligé de modifier tous les champs de votre ligne concernant le serveur que vous voulez modifier. Vous pouvez par exemple seulement changer le port en précisant `new_port` en plus de l'`alias` obligatoire dans la signature de votre update.

De plus l'id du serveur n'est pas modifiable, il sera peut être généré automatiquement plus tard.


### Auto-Backup

1. #### Création

Vous pouvez créer une auto-backup avec ces différents paramètres :

| Signature : | id_backup | frequency |  name  | timestamp | id_server |   path |
| :---------- | :-------: | :-------: | :----: | :-------: | :-------: | -----: |
| Type :      |  String   |  String   | String |  String   |  String   | String |

Comme ceci :

```
backup = Backup("9", "monthly", "okay", "2021-01-01", "3", "/home/backup")
```

2. #### Suppression

Vous pouvez supprimer une auto-backup grâce à son id de cette manière :

```
Server.delete("9")
```

3. #### Update

Vous pouvez mettre à jour une auto-backup grâce à son id avec ces différents paramètres :

| Signature : |  id_backup  | frequency  |    name    | timestamp  |       path |
| :---------- | :---------: | :--------: | :--------: | :--------: | ---------: |
| Type :      |   String    |   String   |   String   |   String   |     String |
| Règle :     | Obligatoire | Facultatif | Facultatif | Facultatif | Facultatif |

```
Backup.update("9", new_frequency="daily", new_timestamp="2021-01-02", new_path="/home/backup")
```

À noter que vous n'êtes pas obligé de modifier tous les champs de votre ligne concernant l'auto-backup que vous voulez modifier. Vous pouvez par exemple seulement changer le nom en précisant `new_name` en plus de l'`id` obligatoire dans la signature de votre update.

De plus l'id relié au serveur n'est pas modifiable, car la back-up est lié à celui-ci


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

