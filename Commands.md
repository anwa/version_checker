# Some usefull command

## venv

py -m venv .venv
./.venv/scripts/activate
deactivate

## pip

pip install x
pip install x
pip freeze > requirements.txt
pip install -r requirements.txt

## pre-commit

##### Produce a sample .pre-commit-config.yaml file

pre-commit sample-config

##### Install the pre-commit script.

pre-commit install

##### Validate .pre-commit-config.yaml files

pre-commit validate-config

##### Auto-update pre-commit config to the latest repos' versions.

pre-commit autoupdate

##### Run on all the files in the repo.

pre-commit run --all-files

# Usefull links

[filecmp � File and Directory Comparisons](https://docs.python.org/3/library/filecmp.html#module-filecmp)

# VS Code Shortcuts

Ctrl+K Ctrl+0   Fold (collapse) all regions editor.foldAll
Ctrl+K Ctrl+J   Unfold (uncollapse) all regions
