#!/usr/bin/env bash
# This is only used for local development of Misago
python setup.py develop

# Delete project files
rm cron.txt
rm -rf devforum
rm -rf avatargallery
rm -rf static
rm -rf theme
rm -rf media
rm manage.py

# Create new project
python extras/createdevproject.py devforum /srv/misago

# Clean up unnecessary project files
rm -rf theme
rm cron.txt

# Database
./extras/wait_for_postgres.sh
python manage.py migrate

python manage.py runserver 0.0.0.0:8000
