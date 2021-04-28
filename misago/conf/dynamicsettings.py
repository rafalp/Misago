from ..cacheversions import CacheVersions
from ..database.queries import fetch_all
from ..tables import settings
from .types import DynamicSettings, Settings
from .cache import get_settings_cache, set_settings_cache


async def get_dynamic_settings(cache_versions: CacheVersions) -> DynamicSettings:
    settings = await get_settings_cache(cache_versions)
    if settings is None:
        settings = await get_settings_from_db()
        await set_settings_cache(cache_versions, settings)
    return DynamicSettings(settings)


async def get_settings_from_db() -> Settings:
    return {setting["name"]: setting["value"] for setting in await fetch_all(settings)}
