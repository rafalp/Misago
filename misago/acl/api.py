from misago.core import threadstore
from misago.core.cache import cache

from misago.acl import version
from misago.acl.builder import build_acl
from misago.acl.providers import providers


__ALL__ = ['get_user_acl', 'add_acl']


"""
Module functions for ACLS

Workflow for ACLs in Misago is simple:

First, you get user ACL. Its directory that you can introspect to find out user
permissions, or if you have objects, you can use this acl to make those objects
aware of their ACLs. This gives objects themselves special "acl" attribute with
properties defined by ACL providers within their "add_acl_to_target"
"""


def get_user_acl(user):
    """
    Get ACL for User
    """
    acl_key = 'acl_%s' % user.acl_key

    acl_cache = threadstore.get(acl_key)
    if not acl_cache:
        acl_cache = cache.get(acl_key)

    if acl_cache and version.is_valid(acl_cache.get('_acl_version')):
        return acl_cache
    else:
        new_acl = build_acl(user.get_roles())
        new_acl['_acl_version'] = version.get_version()

        threadstore.set(acl_key, new_acl)
        cache.set(acl_key, new_acl)

        return new_acl


def add_acl(user, target):
    """
    Add valid ACL to target (iterable of objects or single object)
    """
    try:
        for item in target:
            _add_acl_to_target(user, target)
    except TypeError:
        _add_acl_to_target(user, target)


def _add_acl_to_target(user, target):
    """
    Add valid ACL to single target, helper for add_acl function
    """
    target.acl = {}

    for extension, module in providers.list():
        if hasattr(module, 'add_acl_to_target'):
            module.add_acl_to_target(user, user.acl, target)
