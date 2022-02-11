from asyncio import iscoroutinefunction
from functools import wraps

from ..conf.dynamicsettings import DynamicSettings


class override_dynamic_settings:
    def __init__(self, **settings):
        self._overrides = settings

    async def __aenter__(self):
        DynamicSettings.override_settings(self._overrides)

    async def __aexit__(self, *_):
        DynamicSettings.remove_overrides()

    def __enter__(self):
        DynamicSettings.override_settings(self._overrides)

    def __exit__(self, *_):
        DynamicSettings.remove_overrides()

    def __call__(self, f):
        if iscoroutinefunction(f):
            return self.wrap_async_function(f)

        return self.wrap_function(f)

    def wrap_async_function(self, f):
        @wraps(f)
        async def test_function_wrapper(*args, **kwargs):
            async with self:
                return await f(*args, **kwargs)

        return test_function_wrapper

    def wrap_function(self, f):
        @wraps(f)
        def test_function_wrapper(*args, **kwargs):
            with self:
                return f(*args, **kwargs)

        return test_function_wrapper
