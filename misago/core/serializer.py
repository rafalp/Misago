import base64
from hashlib import sha256

from django.conf import settings


try:
    import cPickle as pickle
except ImportError:
    import pickle



def _checksum(base):
    return sha256(('%s+%s' % (settings.SECRET_KEY, base)).encode()).hexdigest()[:14]


def loads(dry):
    checksum = dry[:14]
    base = dry[14:]

    if _checksum(base) == checksum:
        return pickle.loads(base64.decodestring(base.encode()))
    else:
        raise ValueError("pickle checksum is invalid")


def dumps(wet):
    from misago.core.deprecations import warn
    warn('misago.core.serializer is being replaced with json')
    base = base64.encodestring(pickle.dumps(wet, pickle.HIGHEST_PROTOCOL)).decode()
    checksum = _checksum(base)
    return '%s%s' % (checksum, base)


def regenerate_checksum(dry):
    base = dry[14:]
    checksum = _checksum(base)
    return '%s%s' % (checksum, base)
