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
