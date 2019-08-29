from typing import Any, Dict, Optional

TRUE_STR_VALUES = ("true", "yes", "y", "on")
OVERRIDABLE_SETTINGS = (
    "debug",
    "database_url",
    "cache_url",
    "static_root",
    "media_root",
    "plugins",
)


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
        self._debug = settings.get("MISAGO_DEBUG", "").lower() in TRUE_STR_VALUES
        self._test = settings.get("MISAGO_TEST", "").lower() in TRUE_STR_VALUES

        self._database_url = settings.get("MISAGO_DATABASE_URL")
        self._cache_url = settings.get("MISAGO_CACHE_URL")

        self._static_root = settings.get("MISAGO_STATIC_ROOT")
        self._media_root = settings.get("MISAGO_MEDIA_ROOT")

        self._plugins = settings.get("MISAGO_PLUGINS")

    @classmethod
    def override_settings(cls, overrides):
        for name, value in overrides.items():
            assert (
                name.lower() in OVERRIDABLE_SETTINGS
            ), f"overriding '{name}' setting is not supported"
            cls._overrides[name.lower()] = value

    @classmethod
    def remove_overrides(cls):
        cls._overrides = {}

    @property
    def debug(self) -> bool:
        return self._overrides.get("debug", self._debug)

    @property
    def test(self) -> bool:
        return self._test

    @property
    def database_url(self) -> str:
        return self._overrides.get("database_url", self._database_url)

    @property
    def cache_url(self) -> str:
        return self._overrides.get("cache_url", self._cache_url)

    @property
    def static_root(self) -> str:
        return self._overrides.get("static_root", self._static_root)

    @property
    def media_root(self) -> str:
        return self._overrides.get("media_root", self._media_root)

    @property
    def plugins(self) -> str:
        return self._overrides.get("plugins", self._plugins)
