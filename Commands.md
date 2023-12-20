# Some usefull command

## venv

```bash
python -m venv .venv
./.venv/scripts/activate
deactivate
```

## pip

```bash
pip install x
pip uninstall x
pip freeze > requirements.txt
pip install -r requirements.txt
```

## pre-commit

##### Produce a sample .pre-commit-config.yaml file

```bash
pre-commit sample-config
```

##### Install the pre-commit script.

```bash
pre-commit install
```

##### Validate .pre-commit-config.yaml files

```bash
pre-commit validate-config
```

##### Auto-update pre-commit config to the latest repos' versions.

```bash
pre-commit autoupdate
```

##### Run on all the files in the repo.

```bash
pre-commit run --all-files
```

# Usefull links

[filecmp - File and Directory Comparisons](https://docs.python.org/3/library/filecmp.html#module-filecmp)

# VS Code Shortcuts

<kbd>Ctrl+K</kbd> <kbd>Ctrl+0</kbd> Ctrl+K Ctrl+0   Fold (collapse) all regions editor.foldAll
<kbd>Ctrl+K</kbd> <kbd>Ctrl+J</kbd> Unfold (uncollapse) all regions
