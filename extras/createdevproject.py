"""
Creates a test project for local development
"""

import os
import sys

from misago.core import setup


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    project_name = 'forum'

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

        s = s.replace("'NAME': '',", "'NAME': os.environ['POSTGRES_DB'],")
        s = s.replace("'USER': '',", "'USER': os.environ['POSTGRES_USER'],")
        s = s.replace("'PASSWORD': '',", "'PASSWORD': os.environ['POSTGRES_PASSWORD'],")
        s = s.replace("'HOST': 'localhost',", "'HOST': os.environ['POSTGRES_HOST'],")

    with open(f, 'w') as fd:
        fd.write(s)


if __name__ == '__main__':
    main()
