from ..cache import cache
from ..cacheversions import invalidate_cache
from ..types import CacheVersions, Settings
from . import SETTINGS_CACHE


async def get_settings_cache(cache_versions: CacheVersions) -> Settings:
    return await cache.get(SETTINGS_CACHE, version=cache_versions["settings"])


async def set_settings_cache(cache_versions: CacheVersions, settings: Settings):
    await cache.set(SETTINGS_CACHE, settings, version=cache_versions["settings"])


async def clear_settings_cache():
    await invalidate_cache(SETTINGS_CACHE)
