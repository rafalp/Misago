from typing import Any, Dict, Optional

from . import defaults


class StaticSettings:
    _is_setup: bool
    _conf: Dict[str, Any]
    _overrides: Dict[str, Any] = {}

    def __init__(self):
        self._is_setup = False
        self._conf = {}

    def setup(self, settings_module: object):
        assert not self._is_setup, "'setup()' was already called"

        for key, value in settings_module.__dict__.items():
            if key != key.upper():
                continue
            self._conf[key] = value

        self._is_setup = True

    def __getattr__(self, setting: str) -> Any:
        assert self._is_setup, "'StaticSettings' instance has to be setup first"

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
