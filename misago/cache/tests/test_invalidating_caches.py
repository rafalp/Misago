from unittest.mock import patch

from django.test import TestCase

from misago.cache.cache import (
    CACHE_NAME, get_cache_versions_from_db, invalidate_cache, invalidate_all_caches
)
from misago.cache.models import CacheVersion


def cache_version():
    return CacheVersion.objects.create(cache="test_cache")


class InvalidatingCacheTests(TestCase):
    @patch('django.core.cache.cache.delete')
    def test_invalidating_cache_updates_cache_version_in_database(self, _):
        test_cache = cache_version()
        invalidate_cache(test_cache.cache)
        updated_test_cache = CacheVersion.objects.get(cache=test_cache.cache)
        assert test_cache.version != updated_test_cache.version

    @patch('django.core.cache.cache.delete')
    def test_invalidating_cache_deletes_versions_cache(self, cache_delete):
        test_cache = cache_version()
        invalidate_cache(test_cache.cache)
        cache_delete.assert_called_once_with(CACHE_NAME)

    @patch('django.core.cache.cache.delete')
    def test_invalidating_all_caches_updates_cache_version_in_database(self, _):
        test_cache = cache_version()
        invalidate_all_caches()
        updated_test_cache = CacheVersion.objects.get(cache=test_cache.cache)
        assert test_cache.version != updated_test_cache.version

    @patch('django.core.cache.cache.delete')
    def test_invalidating_all_caches_deletes_versions_cache(self, cache_delete):
        cache_version()
        invalidate_all_caches()
        cache_delete.assert_called_once_with(CACHE_NAME)
