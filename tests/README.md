## Windows change execution of scripts permissions

```
Set-ExecutionPolicy -ExecutionPolicy AllSigned -Scope CurrentUser
```

### List permissions

```
Get-ExecutionPolicy -List
```

## Enter into virtual environment

```
.venv\Scripts\activate
```

## Create venv

```
python -m venv .venv
```
