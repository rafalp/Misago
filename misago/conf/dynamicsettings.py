from ..database.queries import fetch_all
from ..tables import settings
from ..types import CacheVersions, Setting, Settings
from .cache import get_settings_cache, set_settings_cache


async def get_dynamic_settings(cache_versions: CacheVersions) -> "DynamicSettings":
    settings = await get_settings_cache(cache_versions)
    if settings is None:
        settings = await get_settings_from_db()
        await set_settings_cache(cache_versions, settings)
    return DynamicSettings(settings)


async def get_settings_from_db() -> Settings:
    return {setting["name"]: setting["value"] for setting in await fetch_all(settings)}


class DynamicSettings(Settings):
    _overrides: Settings = {}

    def __getitem__(self, setting: str) -> Setting:
        if setting in self._overrides:
            return self._overrides[setting]
        try:
            return super().__getitem__(setting)
        except KeyError:
            raise KeyError(f"Setting '{setting}' is not defined.")

    @classmethod
    def override_settings(cls, overrides: Settings):
        cls._overrides = overrides

    @classmethod
    def remove_overrides(cls):
        cls._overrides = {}
