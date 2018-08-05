#!/usr/bin/env python
import os
import pwd
import shutil
import sys

from django import setup


TEST_RUNNER_PATH = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def runtests():
    args, kwargs = parse_args()
    setup_testproject()
    run_django(*args, **kwargs)


def parse_args():
    args = []
    kwargs = {
        'verbosity': 1,
        'noinput': True,
    }

    sys_argv = sys.argv[1:]
    if sys_argv and sys_argv[0] == 'test':
        sys_argv = sys_argv[1:]

    for arg in sys_argv:
        if arg == '--verbose':
            kwargs['verbosity'] = 2
        else:
            args.append(arg)

    return args, kwargs


def setup_testproject():
    project_template_path = os.path.join(TEST_RUNNER_PATH, 'misago/project_template')

    test_project_path = os.path.join(TEST_RUNNER_PATH, "testproject")
    if os.path.exists(test_project_path):
        shutil.rmtree(test_project_path)

    shutil.copytree(project_template_path, test_project_path)

    module_init_path = os.path.join(test_project_path, '__init__.py')
    with open(module_init_path, "w") as py_file:
        py_file.write('')

    settings_path = os.path.join(
        test_project_path, 'project_name', 'settings.py')

    with open(settings_path, "r") as py_file:
        settings_file = py_file.read()

        # Do some configuration magic
        settings_file = settings_file.replace('{{ project_name }}', 'testproject.project_name')
        settings_file = settings_file.replace('{{ secret_key }}', 't3stpr0j3ct')

        settings_file += """
# disable account validation via Stop Forum Spam
MISAGO_NEW_REGISTRATIONS_VALIDATORS = (
    'misago.users.validators.validate_gmail_email',
)

# store mails in memory
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# use in-memory cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'uniqu3-sn0wf14k3'
    }
}

# Use MD5 password hashing to speed up test suite
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

# Default misago address to test address
MISAGO_ADDRESS = 'http://testserver/'

# Use english search config
MISAGO_SEARCH_CONFIG = 'english'


# Register test post validator
MISAGO_POST_VALIDATORS = [
    'misago.core.testproject.validators.test_post_validator',
]


# Register test post search filter
MISAGO_POST_SEARCH_FILTERS = [
    'misago.core.testproject.searchfilters.test_filter',
]
"""

    if os.environ.get('TRAVIS'):
        settings_file += """

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'travis_ci_test',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

TEST_NAME = 'travis_ci_test'
"""
    else:
        settings_file += """
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['POSTGRES_TEST_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': os.environ['POSTGRES_HOST'],
        'PORT': 5432,
    }
}
"""

    with open(settings_path, "w") as py_file:
        py_file.write(settings_file)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testproject.project_name.settings")


def run_django(*args, **kwargs):
    setup()

    from django.core.management import call_command
    sys.exit(call_command('test', *args, **kwargs))


if __name__ == '__main__':
    runtests()
