from functools import wraps

from misago.conf.databasesettings import DatabaseSettings


class OverrideDatabaseSettings:
    def __init__(self, **settings):
        self._overrides = settings

    def __enter__(self):
        DatabaseSettings.override_settings(self._overrides)

    def __exit__(self, *_):
        DatabaseSettings.remove_overrides()

    def __call__(self, f):
        @wraps(f)
        def test_function_wrapper(*args, **kwargs):
            with self as context:
                return f(*args, **kwargs)
        return test_function_wrapper