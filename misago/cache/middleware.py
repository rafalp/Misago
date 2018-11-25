from django.core.cache import cache
from django.utils.functional import SimpleLazyObject

from . import CACHE_NAME
from .models import CacheVersion


def cache_versions_middleware(get_response):
    """Sets request.cache_versions attribute with dict of cache versions."""
    def middleware(request):
        request.cache_versions = SimpleLazyObject(get_cache_versions)
        return get_response(request)

    return middleware


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