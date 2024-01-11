# KDNA

This is the official repository for the DO2023-2026 python CLI backup project

Après avoir cloné le dépôt, vous devrez installer toutes les dépendances

### Start the app

```bash
poetry run python KDNA/__init__.py
```

### Run the tests

```bash
poetry run pytest tests
```

OU 

```bash
make test
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


