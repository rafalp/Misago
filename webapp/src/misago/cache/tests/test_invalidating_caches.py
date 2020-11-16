from ..models import CacheVersion
from ..versions import invalidate_all_caches, invalidate_cache


def test_invalidating_cache_updates_cache_version_in_database(cache_version):
    invalidate_cache(cache_version.cache)
    updated_cache_version = CacheVersion.objects.get(cache=cache_version.cache)
    assert cache_version.version != updated_cache_version.version


def test_invalidating_all_caches_updates_cache_version_in_database(cache_version):
    invalidate_all_caches()
    updated_cache_version = CacheVersion.objects.get(cache=cache_version.cache)
    assert cache_version.version != updated_cache_version.version
