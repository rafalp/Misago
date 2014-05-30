from misago.core import cachebuster as cb


ACL_CACHE_NAME = 'misago_acl'


def get_version():
    return cb.get_version(ACL_CACHE_NAME)


def is_valid(version):
    return cb.is_valid(ACL_CACHE_NAME, version)


def invalidate():
    cb.invalidate(ACL_CACHE_NAME)

