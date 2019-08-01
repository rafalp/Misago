import os
from importlib import import_module

__version__ = "4.0"
__released__ = False


def setup():
    from .conf import SETTINGS_VARIABLE_NAME, settings

    try:
        settings_module_name = os.environ.get(SETTINGS_VARIABLE_NAME)
        if not settings_module_name:
            raise ValueError(
                f"'{SETTINGS_VARIABLE_NAME}' env variable is not defined or empty"
            )

        settings_module = import_module(settings_module_name)
    except ImportError:
        raise ImportError(f"'{settings_module_name}' module could not be imported")
    else:
        settings.setup(settings_module)
