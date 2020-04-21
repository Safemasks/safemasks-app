# Safemasks app

Django web app and API interface for Safemasks project

## Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Running development server

This app needs the following two environment variables to work
```bash
export SAFEMASKS_ENVIRONMENT="DEBUG"
export SAFEMASKS_SECRET_KEY="super-complicated-password"
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
Note that reviews will only be populated if the review table is empty.
