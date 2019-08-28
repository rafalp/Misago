from typing import Any, Dict, Optional

TRUE_STR_VALUES = ("true", "yes", "y", "on")


class StaticSettings:
    _overrides: Dict[str, Any] = {}

    _debug: bool
    _test: bool

    _database_url: Optional[str]
    _cache_url: Optional[str]

    _static_root: Optional[str]
    _media_root: Optional[str]

    _plugins: Optional[str]

    def __init__(self, settings: Dict[str, Any]):
        self._debug = settings.get("MISAGO_DEBUG", "").lowercase() in TRUE_STR_VALUES
        self._test = settings.get("MISAGO_TEST", "").lowercase() in TRUE_STR_VALUES

        self._database_url = settings.get("MISAGO_DATABASE_URL")
        self._cache_url = settings.get("MISAGO_CACHE_URL")

        self._static_root = settings.get("MISAGO_STATIC_ROOT")
        self._media_root = settings.get("MISAGO_MEDIA_ROOT")

        self._plugins = settings.get("MISAGO_PLUGINS")

    @classmethod
    def override_settings(cls, overrides):
        cls._overrides = overrides

    @classmethod
    def remove_overrides(cls):
        cls._overrides = {}

    @property
    def debug(self) -> bool:
        return self._overrides.get("DEBUG", self._debug)

    @property
    def test(self) -> bool:
        return self._test

    @property
    def database_url(self) -> str:
        return self._overrides.get("DATABASE_URL", self._database_url)

    @property
    def cache_url(self) -> str:
        return self._overrides.get("CACHE_URL", self._cache_url)

    @property
    def static_root(self) -> str:
        return self._overrides.get("STATIC_ROOT", self.static_root)

    @property
    def media_root(self) -> str:
        return self._overrides.get("MEDIA_ROOT", self._media_root)

    @property
    def plugins(self) -> str:
        return self._overrides.get("PLUGINS", self._plugins)
