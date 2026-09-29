#!/usr/bin/env bash
set -e

sudo service postgresql start
flask --app flaskr run --debug
