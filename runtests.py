import os
import pwd
import shutil
import sys

from django import setup
from django.test.utils import setup_test_environment


def runtests():
    args, kwargs = parse_args()
    setup_testproject()
    run_django(*args, **kwargs)


def parse_args():
    args = sys.argv[1:]
    kwargs = {
        'verbosity': 1,
        'noinput': True,
    }

    if args and args[0] == 'test':
        args = args[1:]

    for arg in sys_argv:
        if arg == '--verbose':
            kwargs['verbosity'] = 2
        else:
            args.append(arg)

    return args, kwargs


def setup_testproject():
    test_runner_path = os.path.dirname(os.path.abspath(__file__))
    project_template_path = os.path.join(test_runner_path, 'misago/project_template')
    project_package_path = os.path.join(test_runner_path, 'misago/project_template/project_name')

    test_project_path = os.path.join(test_runner_path, "testproject")
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
# disable account validation via API's
MISAGO_NEW_REGISTRATIONS_VALIDATORS = ()

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
        'NAME': 'misago_test',
        'USER': '%s',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
""" % pwd.getpwuid(os.getuid())[0]

    with open(settings_path, "w") as py_file:
        py_file.write(settings_file)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testproject.project_name.settings")


def run_django(*args, **kwargs):
    setup()
    setup_test_environment()

    from django.core.management.commands import test
    sys.exit(test.Command().execute(*args, **kwargs))


if __name__ == '__main__':
    runtests()
