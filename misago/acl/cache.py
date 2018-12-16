from django.core.cache import cache

from misago.cache.versions import invalidate_cache

from . import ACL_CACHE


def get(user, cache_versions):
    key = get_cache_key(user, cache_versions)
    return cache.get(key)


def set(user, cache_versions, user_acl):
    key = get_cache_key(user, cache_versions)
    cache.set(key, user_acl)


def get_cache_key(user, cache_versions):
    return 'acl_%s_%s' % (user.acl_key, cache_versions[ACL_CACHE])


def clear():
    invalidate_cache(ACL_CACHE)
