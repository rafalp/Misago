#!/usr/bin/env bash
# This is only used for local development of Misago in Docker
# Execute from the root of the project ./extras/init.sh
python setup.py develop

# Create new project
python extras/createdevproject.py devforum /srv/misago

# Clean up unnecessary project files
rm -rf theme
rm cron.txt

# Database
./extras/wait_for_postgres.sh
python manage.py migrate
python extras/createsuperuser.py
