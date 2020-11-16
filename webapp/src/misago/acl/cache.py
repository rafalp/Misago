from django.core.cache import cache

from . import ACL_CACHE
from ..cache.versions import invalidate_cache


def get_acl_cache(user, cache_versions):
    key = get_cache_key(user, cache_versions)
    return cache.get(key)


def set_acl_cache(user, cache_versions, user_acl):
    key = get_cache_key(user, cache_versions)
    cache.set(key, user_acl)


def get_cache_key(user, cache_versions):
    return "acl_%s_%s" % (user.acl_key, cache_versions[ACL_CACHE])


def clear_acl_cache():
    invalidate_cache(ACL_CACHE)
