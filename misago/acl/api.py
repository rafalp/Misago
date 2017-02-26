"""
Module functions for ACLs

Workflow for ACLs in Misago is simple:

First, you get user ACL. Its directory that you can introspect to find out user
permissions, or if you have objects, you can use this acl to make those objects
aware of their ACLs. This gives objects themselves special "acl" attribute with
properties defined by ACL providers within their "add_acl_to_target"
"""
import copy

from misago.core import threadstore
from misago.core.cache import cache

from . import version
from .builder import build_acl
from .providers import providers


def get_user_acl(user):
    """get ACL for User"""
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
    """add valid ACL to target (iterable of objects or single object)"""
    if hasattr(target, '__iter__'):
        for item in target:
            _add_acl_to_target(user, item)
    else:
        _add_acl_to_target(user, target)


def _add_acl_to_target(user, target):
    """add valid ACL to single target, helper for add_acl function"""
    target.acl = {}

    for annotator in providers.get_type_annotators(target):
        annotator(user, target)


def serialize_acl(target):
    """serialize authenticated user's ACL"""
    serialized_acl = copy.deepcopy(target.acl_cache)

    for serializer in providers.get_type_serializers(target):
        serializer(serialized_acl)

    return serialized_acl
