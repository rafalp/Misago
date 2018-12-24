from functools import wraps

from .dynamicsettings import DynamicSettings


class override_dynamic_settings:
    def __init__(self, **settings):
        self._overrides = settings

    def __enter__(self):
        DynamicSettings.override_settings(self._overrides)

    def __exit__(self, *_):
        DynamicSettings.remove_overrides()

    def __call__(self, f):
        @wraps(f)
        def test_function_wrapper(*args, **kwargs):
            with self:
                return f(*args, **kwargs)

        return test_function_wrapper
