from django.core.cache import cache

from . import MENU_LINKS_CACHE
from ..cache.versions import invalidate_cache


def get_menus_cache(cache_versions):
    key = get_cache_key(cache_versions)
    return cache.get(key)


def set_menus_cache(cache_versions, menu_links):
    key = get_cache_key(cache_versions)
    cache.set(key, menu_links)


def get_cache_key(cache_versions):
    return "%s_%s" % (MENU_LINKS_CACHE, cache_versions[MENU_LINKS_CACHE])


def clear_menus_cache():
    invalidate_cache(MENU_LINKS_CACHE)
