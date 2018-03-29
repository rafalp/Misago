#!/usr/bin/env bash
# This is only used for local development of Misago
python setup.py develop
python extras/createdevproject.py
./extras/wait_for_postgres.sh
python forum/manage.py migrate
python forum/manage.py runserver 0.0.0.0:8000
