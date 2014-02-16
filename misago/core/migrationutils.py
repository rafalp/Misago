from importlib import import_module
from django.utils import translation
from misago.core.cache import cache as default_cache
from misago.core.cachebuster import CACHE_KEY


def ugettext_lazy(string):
    """
    Custom wrapper that preserves untranslated message on lazy translation
    string object, useful for db entries that should be found by makemessages
    and stored untranslated
    """
    t = translation.ugettext_lazy(string)
    t.message = string
    return t


def with_core_models(migration, this_migration=None):
    module_name = 'misago.core.migrations.%s' % migration
    migration_module = import_module(module_name)
    core_models = migration_module.Migration.models

    if this_migration:
        core_models.update(this_migration)
    return core_models


def cachebuster_register_cache(orm, cache):
    orm['core.CacheVersion'].objects.create(cache=cache)


def cachebuster_unregister_cache(orm, cache):
    try:
        cache = orm['core.CacheVersion'].objects.get(cache=cache)
        cache.delete()
    except orm['core.CacheVersion'].DoesNotExist:
        raise ValueError('Cache "%s" is not registered' % cache)


def delete_cachebuster_cache():
    default_cache.delete(CACHE_KEY)
