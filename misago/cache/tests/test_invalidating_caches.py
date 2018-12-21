import pytest

from misago.cache.versions import (
    CACHE_NAME, invalidate_cache, invalidate_all_caches
)
from misago.cache.models import CacheVersion


@pytest.fixture
def cache_delete(mocker):
    return mocker.patch('django.core.cache.cache.delete')


def test_invalidating_cache_updates_cache_version_in_database(cache_delete, cache_version):
    invalidate_cache(cache_version.cache)
    updated_cache_version = CacheVersion.objects.get(cache=cache_version.cache)
    assert cache_version.version != updated_cache_version.version


def test_invalidating_cache_deletes_versions_cache(cache_delete, cache_version):
    invalidate_cache(cache_version.cache)
    cache_delete.assert_called_once_with(CACHE_NAME)


def test_invalidating_all_caches_updates_cache_version_in_database(cache_delete, cache_version):
    invalidate_all_caches()
    updated_cache_version = CacheVersion.objects.get(cache=cache_version.cache)
    assert cache_version.version != updated_cache_version.version


def test_invalidating_all_caches_deletes_versions_cache(cache_delete, cache_version):
    invalidate_all_caches()
    cache_delete.assert_called_once_with(CACHE_NAME)
