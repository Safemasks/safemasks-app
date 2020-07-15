#!/usr/bin/env bash
set -e

## run tests
safemasks test

## run checks
###ToDo: Set to warning level on later stage
safemasks check --deploy --fail-level ERROR

##migrate django db
safemasks migrate

## collect all static before run
safemasks collectstatic --noinput

##Compile localization files
safemasks compilemessages

git clone https://github.com/letsencrypt/letsencrypt ./letsencrypt

#run the installation , nginx config for SSL has been set up in entrypoint.sh
./letsencrypt/letsencrypt-auto certonly --standalone --email $DOMAINEMAIL --agree-tos --no-eff-email -d $DOMAIN

##migrate django db
python manage.py migrate


## collect all static before run
python manage.py collectstatic

## Run server
python manage.py runserver 0.0.0.0:90