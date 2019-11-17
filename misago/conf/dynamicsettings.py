from typing import Any, Dict

from ..database.queries import fetch_all
from ..tables import settings
from ..types import CacheVersions, Setting, SettingValue, Settings
from .cache import get_settings_cache, set_settings_cache
from .serializers import deserialize_value


async def get_dynamic_settings(cache_versions: CacheVersions) -> "DynamicSettings":
    settings = await get_settings_cache(cache_versions)
    if settings is None:
        settings = await get_settings_from_db()
        await set_settings_cache(cache_versions, settings)
    return DynamicSettings(settings)


async def get_settings_from_db() -> Settings:
    data = {}
    for setting in await fetch_all(settings):
        if setting["python_type"] == "image":
            data[setting["name"]] = Setting(
                value=deserialize_value(setting["python_type"], setting["value"]),
                width=setting["width"],
                height=setting["height"],
            )
        else:
            data[setting["name"]] = Setting(
                value=deserialize_value(setting["python_type"], setting["value"]),
                width=None,
                height=None,
            )

    return data


class DynamicSettings:
    _settings: Settings
    _overrides: Dict[str, SettingValue] = {}

    def __init__(self, settings: Settings):
        self._settings = settings

    def get(self, setting: str) -> Setting:
        if setting in self._settings:
            return self._settings[setting]
        raise AttributeError(f"Setting '{setting}' is not defined.")

    def items(self) -> Dict[str, SettingValue]:
        settings = {setting: data["value"] for setting, data in self._settings.items()}
        if self._overrides:
            settings.update(self._overrides)
        return settings

    def __getattr__(self, setting: str) -> Any:
        if setting in self._overrides:
            return self._overrides[setting]
        if setting in self._settings:
            return self._settings[setting]["value"]
        raise AttributeError(f"Setting '{setting}' is not defined.")

    @classmethod
    def override_settings(cls, overrides: Dict[str, SettingValue]):
        cls._overrides = overrides

    @classmethod
    def remove_overrides(cls):
        cls._overrides = {}
