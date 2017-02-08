from misago.core import cachebuster

from .constants import ACL_CACHEBUSTER


def get_version():
    return cachebuster.get_version(ACL_CACHEBUSTER)


def is_valid(version):
    return cachebuster.is_valid(ACL_CACHEBUSTER, version)


def invalidate():
    cachebuster.invalidate(ACL_CACHEBUSTER)
