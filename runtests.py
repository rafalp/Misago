import os
import pwd
import shutil
import sys

from django import setup
from django.test.utils import setup_test_environment


def runtests():
    test_runner_path = os.path.dirname(__file__)
    project_template_path = os.path.join(
        test_runner_path, 'misago/project_template')
    project_package_path = os.path.join(
        test_runner_path, 'misago/project_template/project_name')

    test_project_path = os.path.join(test_runner_path, "testproject")
    if not os.path.exists(test_project_path):
        shutil.copytree(project_template_path, test_project_path)
        for filename in os.listdir(project_package_path):
            src_path = os.path.join(project_package_path, filename)
            dst_path = os.path.join(test_project_path, filename)
            shutil.copy2(src_path, dst_path)

        settings_path = os.path.join(test_project_path, "settings.py")
        with open(settings_path, "r") as py_file:
            settings_file = py_file.read()

            # Do some configuration magic

            settings_file = settings_file.replace(
                "os.path.dirname(os.path.dirname(__file__))",
                "os.path.dirname(__file__)")

            settings_file = settings_file.replace("{{ project_name }}",
                                                   "testproject")
            settings_file = settings_file.replace("{{ secret_key }}",
                                                  "t3stpr0j3ct")
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
        'NAME': 'misago_postgres',
        'USER': '%s',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
""" % pwd.getpwuid(os.getuid())[0]

        with open(settings_path, "w") as py_file:
            py_file.write(settings_file)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testproject.settings")

    setup()
    setup_test_environment()

    if __name__ == '__main__':
        args = sys.argv[1:]
    else:
        args = []

    from django.core.management.commands import test
    sys.exit(test.Command().execute(*args, verbosity=1, noinput=True))


if __name__ == '__main__':
    runtests()
