from django.utils import translation
from misago.core.cache import cache


def ugettext_lazy(string):
    """
    Custom wrapper that preserves untranslated message on lazy translation
    string object, useful for db entries that should be found by makemessages
    and stored untranslated
    """
    t = translation.ugettext_lazy(string)
    t.message = string
    return t


def cachebuster_register_cache(orm, cache):
    orm.CacheVersion.objects.create(cache=cache)


def cachebuster_unregister_cache(orm, cache):
    try:
        cache = orm.CacheVersion.objects.get(cache=cache)
        cache.delete()
    except orm.CacheVersion.DoesNotExist:
        raise ValueError('Cache "%s" is not registered' % cache)


def prune_cachebuster_cache():
    default_cache.clear()
