from importlib import import_module
from typing import Any, Dict

from . import defaults


class StaticConf:
    _conf: Dict[str, Any]
    _overrides: Dict[str, Any] = {}

    @classmethod
    def override_settings(cls, overrides):
        cls._overrides = overrides

    @classmethod
    def remove_overrides(cls):
        cls._overrides = {}

    def __init__(self):
        self._conf = {}

    def configure(self, settings_module: str):
        settings = import_module(settings_module)
        for key, value in settings.__dict__.items():
            if key != key.upper():
                continue
            self._conf[key] = value

    def __getattr__(self, setting: str) -> Any:
        if setting in self._overrides:
            return self._overrides[setting]
        if setting in self._conf:
            return self._conf[setting]
        try:
            return getattr(defaults, setting)
        except AttributeError:
            raise AttributeError(f"Setting '{setting}' is not defined")
