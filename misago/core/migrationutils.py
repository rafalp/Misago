from .cache import cache as default_cache
from .cachebuster import CACHE_KEY


def _CacheVersion(apps):
    return apps.get_model('misago_core', 'CacheVersion')


def cachebuster_register_cache(apps, cache):
    _CacheVersion(apps).objects.create(cache=cache)


def cachebuster_unregister_cache(apps, cache):
    CacheVersion = _CacheVersion(apps)

    try:
        cache = CacheVersion.objects.get(cache=cache)
        cache.delete()
    except CacheVersion.DoesNotExist:
        raise ValueError('Cache "%s" is not registered' % cache)


def delete_cachebuster_cache():
    default_cache.delete(CACHE_KEY)
