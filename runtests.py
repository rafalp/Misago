#!/usr/bin/env python
import os
import sys


def runtests():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devproject.test_settings")
    try:
        from django import setup
        from django.core.management import call_command
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    setup()

    modules = sys.argv[1:]
    if "test" in modules:
        modules.remove("test")

    exit_code = call_command("test", *modules, verbosity=1, noinput=True)
    sys.exit(exit_code)


if __name__ == '__main__':
    runtests()
