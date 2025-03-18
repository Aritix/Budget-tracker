<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./doc/bv-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="./doc/bv-light.png">
  <img alt="Dark or Light Logo" src="./doc/BV_dark.png"  width="full">
</picture>

# BudViz
A budget tracking and visualization tool.

[![Project tests](https://github.com/Aritix/Budget-tracker/actions/workflows/main.yml/badge.svg)](https://github.com/Aritix/Budget-tracker/actions/workflows/main.yml)
[![CodeQL Advanced](https://github.com/Aritix/Budget-tracker/actions/workflows/codeql.yml/badge.svg)](https://github.com/Aritix/Budget-tracker/actions/workflows/codeql.yml)


# Requirements
```
pip install -r requirements.txt
```

# Usage
## Web interface
```
flask --app src/backend/app.py run
```
## Command Line
*Not working at the moment.*
```
py BudViz.py [-h] [-r REFERENCES] [-o OUTPUT] [-d] [--update-refs] input
```
