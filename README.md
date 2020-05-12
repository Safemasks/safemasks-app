# Safemasks app

Django web app and API interface for Safemasks project

## How to deploy to http://safemasks.eastus.cloudapp.azure.com/
- ```git push git push -f origin master```
- Deployment is Automatic. Just wait.
- Just assign these envs in the pipeline. 
- if you dont know what they are, you can find them in keyvault.
- ```environmentVariables :	```
                        - ```SAFEMASKS_HOST ```
                        - ```SAFEMASKS_ENVIRONMENT ```
                        - ```SAFEMASKS_SECRET_KEY ```
                        - ```SAFEMASKS_DB_BACKEND ```
                        - ```SAFEMASKS_DB_HOST ```	
                        - ```SAFEMASKS_DB_PORT 	```
                        - ```SAFEMASKS_DB_ADMIN_USER ```
                        - ```SAFEMASKS_DB_ADMIN_USER_PASSWORD ```
                        - ```SAFEMASKS_DB_NAME ```
                        - ```imagePassword ```


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
