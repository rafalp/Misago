from django.apps import apps
from django.test import TestCase

from misago.core import migrationutils
from misago.core.models import CacheVersion


class CacheBusterUtilsTests(TestCase):
    def test_cachebuster_register_cache(self):
        """cachebuster_register_cache registers cache on migration successfully"""
        cache_name = 'eric_licenses'
        migrationutils.cachebuster_register_cache(apps, cache_name)
        CacheVersion.objects.get(cache=cache_name)

    def test_cachebuster_unregister_cache(self):
        """cachebuster_unregister_cache removes cache on migration successfully"""
        cache_name = 'eric_licenses'
        migrationutils.cachebuster_register_cache(apps, cache_name)
        CacheVersion.objects.get(cache=cache_name)

        migrationutils.cachebuster_unregister_cache(apps, cache_name)
        with self.assertRaises(CacheVersion.DoesNotExist):
            CacheVersion.objects.get(cache=cache_name)

        with self.assertRaises(ValueError):
            migrationutils.cachebuster_unregister_cache(apps, cache_name)
