from django.core.cache import cache

from . import SETTINGS_CACHE
from ..cache.versions import invalidate_cache


def get_settings_cache(cache_versions):
    key = get_cache_key(cache_versions)
    return cache.get(key)


def set_settings_cache(cache_versions, user_settings):
    key = get_cache_key(cache_versions)
    cache.set(key, user_settings)


def get_cache_key(cache_versions):
    return "%s_%s" % (SETTINGS_CACHE, cache_versions[SETTINGS_CACHE])


def clear_settings_cache():
    invalidate_cache(SETTINGS_CACHE)
