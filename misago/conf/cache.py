from django.core.cache import cache

from misago.cache.versions import invalidate_cache

from . import SETTINGS_CACHE


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
