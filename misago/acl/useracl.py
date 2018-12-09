from django.core.cache import cache

from . import buildacl


def get_user_acl(user, cache_versions):
    cache_name = 'acl_%s_%s' % (user.acl_key, cache_versions["acl"])
    user_acl = cache.get(cache_name)
    if user_acl is None:
        user_acl = buildacl.build_acl(user.get_roles())
        cache.set(cache_name, user_acl)
    user_acl["user_id"] = user.id
    user_acl["is_authenticated"] = bool(user.is_authenticated)
    user_acl["is_anonymous"] = bool(user.is_anonymous)
    return user_acl
