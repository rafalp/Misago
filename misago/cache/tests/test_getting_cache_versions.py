from unittest.mock import patch

from django.test import TestCase

from misago.cache.versions import (
    CACHE_NAME, get_cache_versions, get_cache_versions_from_cache, get_cache_versions_from_db
)


class CacheVersionsTests(TestCase):
    def test_db_getter_returns_cache_versions_from_db(self):
        cache_versions = get_cache_versions_from_db()
        assert cache_versions

    @patch('django.core.cache.cache.get', return_value=True)
    def test_cache_getter_returns_cache_versions_from_cache(self, cache_get):
        assert get_cache_versions_from_cache() is True
        cache_get.assert_called_once_with(CACHE_NAME)

    @patch('django.core.cache.cache.get', return_value=True)
    def test_getter_reads_from_cache(self, cache_get):
        assert get_cache_versions() is True
        cache_get.assert_called_once_with(CACHE_NAME)

    @patch('django.core.cache.cache.set')
    @patch('django.core.cache.cache.get', return_value=None)
    def test_getter_reads_from_db_when_cache_is_not_available(self, cache_get, _):
        db_caches = get_cache_versions_from_db()
        assert get_cache_versions() == db_caches
        cache_get.assert_called_once_with(CACHE_NAME)

    @patch('django.core.cache.cache.set')
    @patch('django.core.cache.cache.get', return_value=None)
    def test_getter_sets_new_cache_if_no_cache_is_set(self, _, cache_set):
        get_cache_versions()
        db_caches = get_cache_versions_from_db()
        cache_set.assert_called_once_with(CACHE_NAME, db_caches)

    @patch('django.core.cache.cache.set')
    @patch('django.core.cache.cache.get', return_value=True)
    def test_getter_is_not_setting_new_cache_if_cache_is_set(self, _, cache_set):
        get_cache_versions()
        cache_set.assert_not_called()