# Safemasks app

Django web app and API interface for Safemasks project

For more details see also the docs folder (currently only in German).

## Install dependencies

```bash
python -m pip install -r requirements.txt
python -m pip install [-e] .
```

After this, you can import `safemasks` into other modules and run the `safemasks` CLI which wraps `manage.py`.
Example:
```python
from safemasks.resources.models import Supplier

print(Supplier.objects.all())
```

## Running development server

This app needs the following two environment variables to work
```bash
export SAFEMASKS_ENVIRONMENT="DEBUG"
export SAFEMASKS_SECRET_KEY="super-complicated-password"
export SAFEMASKS_HOST="www.myhost.whatever" # not needed for local host and debug
export SAFEMASKS_DB_BACKEND="sqlite"
export SAFEMASKS_DB_NAME="name of db"
# For non-sqlite data base access
export SAFEMASKS_DB_PORT="5432"
export SAFEMASKS_DB_ADMIN_USER="..."
export SAFEMASKS_DB_ADMIN_USER_PASSWORD="..."
# email
export SAFEMASKS_EMAIL_BACKEND="smtp or console"
# See also https://docs.djangoproject.com/en/3.1/topics/email/#topic-email-backends
# only if smtp
export SAFEMASKS_EMAIL_HOST=...
export SAFEMASKS_EMAIL_HOST_USER=...
export SAFEMASKS_EMAIL_HOST_PASSWORD=...
export SAFEMASKS_EMAIL_USE_SSL=1
export SAFEMASKS_EMAIL_PORT=465
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
visit [http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/), and enter desired information.
Data is stored locally in the database specified by the environment variables for now.
