"""
Modifies the project template to fit with local development
"""
import os
import sys
from misago.core import setup


PROJECT_NAME = 'forum'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    global PROJECT_NAME, SETTINGS_FILE

    # Allow for overriding project name
    if len(sys.argv) > 1:
        PROJECT_NAME = sys.argv[1]
    else:
        sys.argv.append(PROJECT_NAME)

    settings_file = os.path.join(BASE_DIR, PROJECT_NAME, PROJECT_NAME, 'settings.py')

    # Avoid recreating if already present
    if os.path.exists(settings_file):
        return

    setup.start_misago_project()
    tweak_settings(settings_file)


def tweak_settings(f):
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
