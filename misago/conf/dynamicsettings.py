from ..cacheversions import CacheVersions
from ..database import fetch_all_assoc
from ..tables import settings
from .cache import get_settings_cache, set_settings_cache
from .types import DynamicSettings, Settings


async def get_dynamic_settings(cache_versions: CacheVersions) -> DynamicSettings:
    settings = await get_settings_cache(cache_versions)
    if settings is None:
        settings = await get_settings_from_db()
        await set_settings_cache(cache_versions, settings)
    return DynamicSettings(settings)


async def get_settings_from_db() -> Settings:
    rows = await fetch_all_assoc(settings.select(None))
    return {row["name"]: row["value"] for row in rows}
