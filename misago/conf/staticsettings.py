from typing import Any, Dict, List, Optional

TRUE_STR_VALUES = ("true", "yes", "y", "on")
DEFAULT_AVATAR_SIZES = [400, 200, 150, 100, 64, 50, 30]


class StaticSettings:
    _debug: bool

    _test: bool
    _test_database_name: Optional[str]

    _database_url: str
    _cache_url: str

    _static_root: str
    _media_root: str

    _avatar_sizes: List[int]
    _enabled_plugins: Optional[str]

    def __init__(self, settings: Dict[str, Any]):
        self._debug = settings.get("MISAGO_DEBUG", "").lower() in TRUE_STR_VALUES

        self._test = settings.get("MISAGO_TEST", "").lower() in TRUE_STR_VALUES
        self._test_database_name = settings.get("MISAGO_TEST_DATABASE_NAME")

        self._database_url = get_setting_value(settings, "MISAGO_DATABASE_URL")
        self._cache_url = get_setting_value(settings, "MISAGO_CACHE_URL")

        self._static_root = get_setting_value(settings, "MISAGO_STATIC_ROOT")
        self._media_root = get_setting_value(settings, "MISAGO_MEDIA_ROOT")

        self._avatar_sizes = get_avatar_sizes_value(settings, "MISAGO_AVATAR_SIZES")
        self._enabled_plugins = settings.get("MISAGO_ENABLED_PLUGINS", "").strip()

    @property
    def debug(self) -> bool:
        return self._debug

    @property
    def test(self) -> bool:
        return self._test

    @property
    def test_database_name(self) -> Optional[str]:
        return self._test_database_name

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
    def enabled_plugins(self) -> Optional[str]:
        return self._enabled_plugins

    @property
    def avatar_sizes(self) -> List[int]:
        return self._avatar_sizes


def get_setting_value(settings: Dict[str, Any], setting: str) -> Any:
    if not settings.get(setting, "").strip():
        raise ValueError(f"'{setting}' setting has no value")

    return settings[setting]


def get_avatar_sizes_value(settings: Dict[str, Any], setting: str) -> List[int]:
    if not settings.get(setting, "").strip():
        return DEFAULT_AVATAR_SIZES

    try:
        sizes = [int(i.strip()) for i in settings[setting].split(",")]
    except (TypeError, ValueError):
        raise ValueError(
            f"'{setting}' setting should be comma-separated list of integers (40,120,400)"
        )

    return sorted(set(sizes), reverse=True) or DEFAULT_AVATAR_SIZES
