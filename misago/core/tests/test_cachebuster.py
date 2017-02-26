from misago.core import cachebuster
from misago.core.models import CacheVersion
from misago.core.testutils import MisagoTestCase


class CacheBusterTests(MisagoTestCase):
    def test_register_unregister_cache(self):
        """register and unregister adds/removes cache"""
        test_cache_name = 'eric_the_fish'
        with self.assertRaises(CacheVersion.DoesNotExist):
            CacheVersion.objects.get(cache=test_cache_name)

        cachebuster.register(test_cache_name)
        CacheVersion.objects.get(cache=test_cache_name)

        cachebuster.unregister(test_cache_name)
        with self.assertRaises(CacheVersion.DoesNotExist):
            CacheVersion.objects.get(cache=test_cache_name)


class CacheBusterCacheTests(MisagoTestCase):
    def setUp(self):
        super(CacheBusterCacheTests, self).setUp()

        self.cache_name = 'eric_the_fish'
        cachebuster.register(self.cache_name)

    def test_cache_validation(self):
        """cache correctly validates"""
        version = cachebuster.get_version(self.cache_name)
        self.assertEqual(version, 0)

        db_version = CacheVersion.objects.get(cache=self.cache_name).version
        self.assertEqual(db_version, 0)

        self.assertEqual(db_version, version)
        self.assertTrue(cachebuster.is_valid(self.cache_name, version))
        self.assertTrue(cachebuster.is_valid(self.cache_name, db_version))

    def test_cache_invalidation(self):
        """invalidate has increased valid version number"""
        db_version = CacheVersion.objects.get(cache=self.cache_name).version
        cachebuster.invalidate(self.cache_name)

        new_version = cachebuster.get_version(self.cache_name)
        new_db_version = CacheVersion.objects.get(cache=self.cache_name)
        new_db_version = new_db_version.version

        self.assertEqual(new_version, 1)
        self.assertEqual(new_db_version, 1)
        self.assertEqual(new_version, new_db_version)
        self.assertFalse(cachebuster.is_valid(self.cache_name, db_version))
        self.assertTrue(cachebuster.is_valid(self.cache_name, new_db_version))

    def test_cache_invalidation_all(self):
        """invalidate_all has increased valid version number"""
        cache_a = "eric_the_halibut"
        cache_b = "eric_the_crab"
        cache_c = "eric_the_lion"

        cachebuster.register(cache_a)
        cachebuster.register(cache_b)
        cachebuster.register(cache_c)

        cachebuster.invalidate_all()

        new_version_a = CacheVersion.objects.get(cache=cache_a).version
        new_version_b = CacheVersion.objects.get(cache=cache_b).version
        new_version_c = CacheVersion.objects.get(cache=cache_c).version

        self.assertEqual(new_version_a, 1)
        self.assertEqual(new_version_b, 1)
        self.assertEqual(new_version_c, 1)
