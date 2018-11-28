from django.core.cache import cache

from .models import CacheVersion
from .utils import generate_version_string

CACHE_NAME = "cache_versions"


def get_cache_versions():
    cache_versions = get_cache_versions_from_cache()
    if cache_versions is None:
        cache_versions = get_cache_versions_from_db()
        cache.set(CACHE_NAME, cache_versions)
    return cache_versions


def get_cache_versions_from_cache():
    return cache.get(CACHE_NAME)


def get_cache_versions_from_db():
    queryset = CacheVersion.objects.all()
    return {i.cache: i.version for i in queryset}


def invalidate_cache(cache_name):
    CacheVersion.objects.filter(cache=cache_name).update(
        version=generate_version_string(),
    )
    cache.delete(CACHE_NAME)


def invalidate_all_caches():
    for cache_name in get_cache_versions_from_db().keys():
        CacheVersion.objects.filter(cache=cache_name).update(
            version=generate_version_string(),
        )
    cache.delete(CACHE_NAME)
