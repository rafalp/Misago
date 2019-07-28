from importlib import import_module
from typing import Any, Dict

from . import defaults


class StaticConf:
    _is_setup: bool
    _conf: Dict[str, Any]
    _overrides: Dict[str, Any] = {}

    def __init__(self):
        self._is_setup = False
        self._conf = {}

    def setup(self, settings_module: str):
        assert not self._is_setup, "'setup()' was already called"

        settings = import_module(settings_module)
        for key, value in settings.__dict__.items():
            if key != key.upper():
                continue
            self._conf[key] = value

        self._is_setup = True

    def __getattr__(self, setting: str) -> Any:
        assert self._is_setup, "'StaticConf' instance has to be setup first"

        if setting in self._overrides:
            return self._overrides[setting]
        if setting in self._conf:
            return self._conf[setting]
        try:
            return getattr(defaults, setting)
        except AttributeError:
            raise AttributeError(f"Setting '{setting}' is not defined")

    @classmethod
    def override_settings(cls, overrides):
        cls._overrides = overrides

    @classmethod
    def remove_overrides(cls):
        cls._overrides = {}
