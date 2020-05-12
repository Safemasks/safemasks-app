# Safemasks app

Django web app and API interface for Safemasks project

## How to run in Docker for future deploment into container

- Download docker 
- ``` docker build  -f Dockerfile -t safemasks-app .```
- ```docket tag safemasks-app safemasks-app:latest```
- ```docker run -d -p 8000:8000 safemasks-app:latest```



## Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Running development server

This app needs the following two environment variables to work
```bash
export SAFEMASKS_ENVIRONMENT="DEBUG"
export SAFEMASKS_SECRET_KEY="super-complicated-password"
export SAFEMASKS_HOST="www.myhost.whatever" # not needed for local host and debug
export SAFEMASKS_DB_BACKEND="sqlite"
export SAFEMASKS_DB_NAME="name of db"
# You also have to specify other keys like NAME->USER for other backends
```
The super complicated password is used to encrypt sensitive data like user passwords stored in the DB.
To simplify development, this app runs on a local `.sqlite3` backend for now.
Thus you can use whatever password you like.

To initiate the database for the first time, run
```bash
python manage.py migrate
```
in the root directory followed by a

```bash
python manage.py runserver
```
To launch a server.

## Populate initial data

Create a superuser account named admin (some entries require a user to submit)
```bash
python manage.py createsuperuser --username admin
```
and enter infos.
Data is stored locally in an SQLite file for now.

Copy the `Suppliers.xlsx` file to a directory of your choice, e.g., `data/Suppliers.xlsx` and run
```bash
python manage.py initwhitelist data/Suppliers.xlsx
```
from the repo root.
This will populate the whitelist tables.
Similarly,
```bash
python manage.py initblacklist data/Suppliers.xlsx
```
populates the blacklist.
