from django.test import TestCase

from misago.cache.models import CacheVersion
from misago.cache.test import assert_invalidates_cache
from misago.cache.versions import invalidate_cache


class AssertCacheVersionChangedTests(TestCase):
    def test_assertion_fails_if_specified_cache_is_not_invaldiated(self):
        CacheVersion.objects.create(cache="test")
        with self.assertRaises(AssertionError):
            with assert_invalidates_cache("test"):
                pass

    def test_assertion_passess_if_specified_cache_is_invalidated(self):
        CacheVersion.objects.create(cache="test")
        with assert_invalidates_cache("test"):
            invalidate_cache("test")

    def test_assertion_fails_if_other_cache_is_invalidated(self):
        CacheVersion.objects.create(cache="test")
        CacheVersion.objects.create(cache="changed_test")
        with self.assertRaises(AssertionError):
            with assert_invalidates_cache("test"):
                invalidate_cache("changed_test")
