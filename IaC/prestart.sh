#!/usr/bin/env bash
set -e

##migrate django db
python manage.py migrate


## collect all static before run
python manage.py collectstatic


