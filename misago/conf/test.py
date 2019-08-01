from functools import wraps
from typing import Any, Dict, Callable

from .staticsettings import StaticSettings


class override_static_settings:
    def __init__(self, **settings: Dict[str, Any]):
        self._overrides = settings

    def __enter__(self):
        StaticSettings.override_settings(self._overrides)

    def __exit__(self, *_):
        StaticSettings.remove_overrides()

    def __call__(self, f: Callable):
        @wraps(f)
        def test_function_wrapper(*args, **kwargs):
            with self:
                return f(*args, **kwargs)

        return test_function_wrapper
