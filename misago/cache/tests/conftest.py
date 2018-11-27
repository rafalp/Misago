from misago.cache.models import CacheVersion


def cache_version():
    return CacheVersion.objects.create(cache="test_cache")