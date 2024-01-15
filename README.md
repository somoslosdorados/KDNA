# KDNA

As part of the python program, we were responsible for carrying out the KDNA project.

KDNA is a python-coded application for automating and generating document backups on remote servers.
The software works as follows.

First, the application is installed on an X machine by a user with rights to that machine.
Once the software has been installed on a machine, users can connect to it to initialize their configurations.

This configuration is made up of two parts:
- Servers, which are the remote servers to which the user has access.
- Backups, which are instantiated by the user and thus depend on a previously configured server.

Backups, thus created, target a directory or a file, which, on the remote server, will be saved at the root of the user's repository (the one selected during server configuration) on his `/home` directory in a `kdna` folder.

Backups are automated to run recurrently according to their definitions, and are also encrypted by default for security reasons.

## User installation

This is the official repository for the DO2023-2026 python CLI backup project.

### Prerequisites

 - In order to run the project you will need an **SSH key**, *without any password* on this one. This will allow us to connect to the server.


### Install the KDNA project
- ### Option 1 : 
    Without cloning the project run the following line in your terminal :
    ```bash 
    pip install -e "git+https://github.com/somoslosdorados/KDNA.git/#egg=kdna" 
    ```
    To create and initialize the kdna.conf file : 
    ```bash
    kdna server init
    ```

- ### Option 2 :
    You can also install the KDNA project with the following lines :  
    - ### Cloning the project 
    ```bash
    git clone https://github.com/somoslosdorados/KDNA.git
    ```
    - ### Install excecutables

    After cloning the project, you must install all dependencies.
    ```bash
    cd KDNA
    ```
    ```bash
    pip install .
    ```
    To create and initialize the kdna.conf file : 
    ```bash
    kdna server init
    ```


### Common errors on installation 

- #### Error: externally-managed-environment
    See this link if you have this error :
    https://www.makeuseof.com/fix-pip-error-externally-managed-environment-linux/.

### Run the tests

```bash
poetry run pytest
```

### Build the documentation

```bash
sphinx-apidoc -f -o docs/source kdna/
sphinx-build -M html docs/source/ docs/build/
```

## Package added by poetry

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

Once you've finished the installation, you should be able to create local server backups, as well as automatic backups. 

In the following steps we will see how the project works. 

## Commands line
Here you can find all the command you need to manage the project. 

### Help

Get the information you need to use each command
```
kdna <command> --help
kdna <command> <subcommand> --help
```
---
### Server

Managing a backup server

```
kdna server <command> [options] [arguments]
```

- ### Init
    To initialise config file.
    ```bash 
    kdna server init
    ```
- ### Import
    To import server from `.ssh/config` file.
    ```bash
    kdna server ssh_import
    ```
- ### Get status
    To get status of the server.
    ```bash
    kdna server status <alias>
    ```
    | Argument|  Type  |        Description         | Required |
    |:--------|:------:|:--------------------------:|:--------:|
    |         | String |         alias              |   True   |

- ### Add

    Adding a backup server.
    ```
    kdna server add -i <id_server> -ad <libele_connexion> -a <alias_server> -r <repo_backup> -p <port_server>
    ```

    #### Example

    ```
    kdna server add -i S1 -ad kdna@162.38.112.110 -a alias -r /my/repository/backup/ -p 22
    ```

    #### Options

    | Options |  Type  |        Description         | Required |
    |:--------|:------:|:--------------------------:|:--------:|
    | -i      | String |         id_server          |   True   |
    | -ad     | String |    connection label        |   True   |
    | -a      | String |           alias            |   True   |
    | -r      | String |    backup repository       |   True   |
    | -p      | String |            port            |   True   |
    | -e      | Boolean |         encrypt           |   False  |

- ### Delete

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

    > Please note: Only one of the two options must be chosen.

- ### Update

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


- ### List

    List backup servers:

    ```
    kdna server list <project_name>
    ```

    #### Example

    ```
    kdna server list <project_name>
    ```

    #### Options

    | Options |  Type  |   Description    | Required |
    |:--------|:------:|:----------------:|:--------:|
    |         | String |   project_name   |   True   |

---

### Auto-Backup

Manage regular backups

```
kdna auto-backup <command> [options] [arguments]
```

- ### Creation

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


- ### Delete

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


- ### Update

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

    > NOTE : you cannot change the server id, as the backup is linked to it.


- ### List

    List regular backups
    ```
    kdna auto-backup list
    ```
---

### Backup

Managing manual backups

```
kdna backup <command> [options] [arguments]
```

- ### Creation

    Create a backup

    ```
    kdna backup add <project_name> <local_path_backup> <tag> [--prefix <must_generate_an_unique_tag>]
    ``` 

    #### Example

    ```bash
    kdna backup add project /home v1
    ```
    or 
    ```bash
    kdna backup add project /home v1 --prefix true
    ```

    #### Options

    | Options |  Type  | Description | Required |
    |:--------|:------:|:-----------:|:--------:|
    |         | String | project name  |   True   |
    |         | String | path to backup |   True   |
    |         | String | tag name | True |
    |         | Boolean | must generate a unique tag ? | false |


- ### Delete

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


- ### Restore

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


- ### List

    List backups

    ```
    kdna backup list
    ```

---
### Encrypt

Backup encryption management

```
kdna encrypt <command> [options]
```

- ### Generate

    Generate an encryption key

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

- ### Activation

    Activate encryption

    ```
    kdna encrypt activate
    ```

- ### Désactivation

    Desactivate encryption
    ```
    kdna encrypt deactivate
    ```
---

### Tag

Manage tags 

```
kdna tag <command> [options]
```

- ### Creation

    Create a tag

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


- ### List

    List tags

    ```
    kdna tag list
    ```


## kdna.conf file format

This file contains all the data regarding configuration that we want to save.

The configuration file will be automatically created in `~/.kdna/kdna.conf` if it is not present in the project. The file is structured with the following tags:

```
[servers]
[auto-backups]
```

After adding servers/auto-backup, the knda.conf file will contain the following data in order:

```
[servers]
id, address, path, port, alias, encrypted
[auto-backups]
id, frequency, name, timestamp, id_server, path
```

#### Servers
- id: server ID
- address: username@server address
- path: path to the SSH key
- port: port address
- alias: server tag
- encrypted: boolean indicating whether the backups for this server are encrypted

#### Auto-backups
- id: auto-backup ID
- frequency: frequency of auto-backup
- name: name of the auto-backup
- timestamp: date of the last auto-backup
- id_server: ID of the server linked to the auto-backup
- path: local path of the auto-backup

Here's an example of what the file should look like:

```
[servers]
S4, test@debian12.local, /path, 5432, hello, true
[auto-backups]
B2, daily, fezf, 2022-09-02, S2, /home/backup
B3, daily, yes, 2021-09-02, S4, /home/backup
B4, monthly, okay, 2021-01-01, S4, /home/backup
```

## Contributors installation

Follow the instructions for the user option2 installation then you can follow here. 

### Install a virtual environment
In this project, we use the `py venv` virtual environment. Here is the official documentation : https://docs.python.org/3/library/venv.html

Let's create the virtual environment by installing poetry.
```bash
apt install python3-poetry
```


### The pipeline
The CI (Continuous Integration) will activate automatically each time a push or a pull request will append. 

Inside the pipeline we have a job, named build, who will run on the `matrix.plateform`. 
The plateform will define the environnement where we are running the tests.

Here we are testins on three different plateform :
`[ubuntu-latest, macos-latest, windows-latest]`.

On three different versions : `[3.10.11, 3.11.6, 3.12.0]`. 

This bring us to a total of nine test environements (3x3). 

#### Execution of the pipeline : 

1. `- uses: actions/checkout@v1` : we retrieve the project code, the equivalent on doing a `git clone`.

2. `- name: Set up Python ${{ matrix.python-version }}` : we set up python. 

3. `- name: Install dependencies` : we install all the poetry dependencies.

4. `- name: Test with tox` : we run poetry with the tox testing, using this command : `poetry run tox run-parallel`.


#### Command to run the pipeline yourself : 

```bash
poetry run tox run-parallel
```

```bash
#run the pipeline with a specific env
poetry run tox run-parallel -e (env)
```