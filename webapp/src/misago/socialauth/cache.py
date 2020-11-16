from django.core.cache import cache

from . import SOCIALAUTH_CACHE
from ..cache.versions import invalidate_cache


def get_socialauth_cache(cache_versions):
    key = get_cache_key(cache_versions)
    return cache.get(key)


def set_socialauth_cache(cache_versions, socialauth):
    key = get_cache_key(cache_versions)
    cache.set(key, socialauth)


def get_cache_key(cache_versions):
    return "%s_%s" % (SOCIALAUTH_CACHE, cache_versions[SOCIALAUTH_CACHE])


def clear_socialauth_cache():
    invalidate_cache(SOCIALAUTH_CACHE)
