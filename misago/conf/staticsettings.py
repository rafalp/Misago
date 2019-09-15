from typing import Any, Dict, Optional

TRUE_STR_VALUES = ("true", "yes", "y", "on")


class StaticSettings:
    _debug: bool

    _test: bool
    _test_database_url: Optional[str]

    _database_url: Optional[str]
    _cache_url: Optional[str]

    _static_root: Optional[str]
    _media_root: Optional[str]

    _enabled_plugins: Optional[str]

    def __init__(self, settings: Dict[str, Any]):
        self._debug = settings.get("MISAGO_DEBUG", "").lower() in TRUE_STR_VALUES

        self._test = settings.get("MISAGO_TEST", "").lower() in TRUE_STR_VALUES
        self._test_database_url = settings.get("MISAGO_TEST_DATABASE_URL")

        self._database_url = settings.get("MISAGO_DATABASE_URL")
        self._cache_url = settings.get("MISAGO_CACHE_URL")

        self._static_root = settings.get("MISAGO_STATIC_ROOT")
        self._media_root = settings.get("MISAGO_MEDIA_ROOT")

        self._enabled_plugins = settings.get("MISAGO_ENABLED_PLUGINS")

    @property
    def debug(self) -> bool:
        return self._debug

    @property
    def test(self) -> bool:
        return self._test

    @property
    def test_database_url(self) -> str:
        return self._test_database_url

    @property
    def database_url(self) -> str:
        return self._database_url

    @property
    def cache_url(self) -> str:
        return self._cache_url

    @property
    def static_root(self) -> str:
        return self._static_root

    @property
    def media_root(self) -> str:
        return self._media_root

    @property
    def enabled_plugins(self) -> str:
        return self._enabled_plugins
