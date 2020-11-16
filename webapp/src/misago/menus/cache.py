from django.core.cache import cache

from ..cache.versions import invalidate_cache
from . import MENU_ITEMS_CACHE


def get_menus_cache(cache_versions):
    key = get_cache_key(cache_versions)
    return cache.get(key)


def set_menus_cache(cache_versions, menus):
    key = get_cache_key(cache_versions)
    cache.set(key, menus)


def get_cache_key(cache_versions):
    return "%s_%s" % (MENU_ITEMS_CACHE, cache_versions[MENU_ITEMS_CACHE])


def clear_menus_cache():
    invalidate_cache(MENU_ITEMS_CACHE)
