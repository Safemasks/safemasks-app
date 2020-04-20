# Safemasks app

Django web app and API interface for Safemasks project

## Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Running development server

This app needs the following two environment variables to work
```bash
export SAFEMASKS_ENIRONMENT="DEBUG"
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
