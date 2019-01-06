from django.core.cache import cache

from . import THEME_CACHE
from ..cache.versions import invalidate_cache


def get_theme_cache(cache_versions):
    key = get_cache_key(cache_versions)
    return cache.get(key)


def set_theme_cache(cache_versions, theme):
    key = get_cache_key(cache_versions)
    cache.set(key, theme)


def get_cache_key(cache_versions):
    return "%s_%s" % (THEME_CACHE, cache_versions[THEME_CACHE])


def clear_theme_cache():
    invalidate_cache(THEME_CACHE)
