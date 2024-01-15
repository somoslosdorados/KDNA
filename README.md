# KDNA

## PART 1 : User installation

This is the official repository for the DO2023-2026 python CLI backup project.

As part of the python program, we were responsible for carrying out the KDNA project.
This project consists of the creation of local server backups as well as automatic backups.

### Install the KDNA project
```bash
git clone https://github.com/somoslosdorados/KDNA.git
```

### Install a virtual environment
In this project, we use the `py venv` virtual environment. Here is the official documentation : https://docs.python.org/3/library/venv.html

Let's create the virtual environment by installing poetry.
```bash
apt install python3-poetry 
```

### Install all dependencies
After cloning the all project, you must install all dependencies.
```bash
cd KDNA
```
```bash
poetry install
```

### Start the app

```bash
poetry run python kdna/__main__.py
```

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

Once you've finished the istallation, you sould be able to create local server backups, as well as automatic backups. 

In the following steps we will see how the project works. 

## Commands line
[récupérer le README de Pauline].

## kdna.conf file format
deplacer vers le haut ! laisser les details dans contributors!

This file contains all the data regarding configuration that we want to save.

The configuration file will be automatically created in `~/.kdna/kdna.conf` if it is not present in the project. The file is structured with the following tags:

```
[servers]
[auto-backups]
```

After adding servers/auto-backup, the knda.conf file will contain the following data in order:

```
[server]
id, address, path, port, alias, encrypted
[auto-backup]
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

## PART 2 : Contributors installation

Follow the instructions for the user installation then you can follow here. 

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