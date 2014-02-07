from django.core.cache import cache as default_cache
from django.db import models
from misago.core import threadstore


CACHE_KEY = 'misago_cachebuster'


class CacheBusterController(object):
    def register_cache(self, cache):
        from misago.core.models import CacheVersion
        CacheVersion.objects.create(cache=cache)

    def unregister_cache(self, cache):
        from misago.core.models import CacheVersion
        try:
            cache = CacheVersion.objects.get(cache=cache)
            cache.delete()
        except CacheVersion.DoesNotExist:
            raise ValueError('Cache "%s" is not registered' % cache)

    @property
    def cache(self):
        return self.read_threadstore()

    def read_threadstore(self):
        data = threadstore.get(CACHE_KEY, 'nada')
        if data == 'nada':
            data = self.read_cache()
            threadstore.set(CACHE_KEY, data)
        return data

    def read_cache(self):
        data = default_cache.get(CACHE_KEY, 'nada')
        if data == 'nada':
            data = self.read_db()
            default_cache.set(CACHE_KEY, data)
        return data

    def read_db(self):
        from misago.core.models import CacheVersion
        data = {}
        for cache_version in CacheVersion.objects.iterator():
            data[cache_version.cache] = cache_version.version
        return data

    def get_cache_version(self, cache):
        try:
            return self.cache[cache]
        except KeyError:
            raise ValueError('Cache "%s" is not registered' % cache)

    def is_cache_valid(self, cache, version):
        try:
            return self.cache[cache] == version
        except KeyError:
            raise ValueError('Cache "%s" is not registered' % cache)

    def invalidate_cache(self, cache):
        from misago.core.models import CacheVersion
        self.cache[cache] += 1
        CacheVersion.objects.filter(cache=cache).update(
            version=models.F('version') + 1)
        default_cache.delete(CACHE_KEY)

    def invalidate_all(self):
        from misago.core.models import CacheVersion
        CacheVersion.objects.update(version=models.F('version') + 1)
        default_cache.delete(CACHE_KEY)


_controller = CacheBusterController()


# Expose controller API
def register(cache):
    _controller.register_cache(cache)


def unregister(cache):
    _controller.unregister_cache(cache)


def get_version(cache):
    return _controller.get_cache_version(cache)


def is_valid(cache, version):
    return _controller.is_cache_valid(cache, version)


def invalidate(cache):
    _controller.invalidate_cache(cache)


def invalidate_all():
    _controller.invalidate_all()
