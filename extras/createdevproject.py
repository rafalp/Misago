"""
Creates a test project for local development
"""

import os
import sys

from misago.core import setup


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    project_name = 'devforum'

    # Allow for overriding project name
    if len(sys.argv) > 1:
        project_name = sys.argv[1]
    else:
        sys.argv.append(project_name)

    settings_file = os.path.join(BASE_DIR, project_name, 'settings.py')

    # Avoid recreating if already present
    if os.path.exists(settings_file):
        return

    setup.start_misago_project()
    fill_in_settings(settings_file)


def fill_in_settings(f):
    with open(f, 'r') as fd:
        s = fd.read()

        # Postgres
        s = s.replace("'NAME': '',", "'NAME': os.environ['POSTGRES_DB'],")
        s = s.replace("'USER': '',", "'USER': os.environ['POSTGRES_USER'],")
        s = s.replace("'PASSWORD': '',", "'PASSWORD': os.environ['POSTGRES_PASSWORD'],")
        s = s.replace("'HOST': 'localhost',", "'HOST': os.environ['POSTGRES_HOST'],")

        # Specify console backend for email
        s += "\nEMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'\n"

        # Empty the contents of STATICFILES_DIRS (STATICFILES_DIRS = [])
        pos = s.find('STATICFILES_DIRS')
        s = s[:s.find('[', pos) + 1] + s[s.find(']', pos):]

        # Remote theme dir from template dirs
        pos = s.find("'DIRS': [")
        s = s[:s.find('[', pos) + 1] + s[s.find(']', pos):]

    with open(f, 'w') as fd:
        fd.write(s)


if __name__ == '__main__':
    main()
