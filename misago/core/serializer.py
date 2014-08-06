import base64
from hashlib import sha256
try:
    import cPickle as pickle
except ImportError:
    import pickle

from django.conf import settings


def _checksum(base):
    return sha256('%s+%s' % (settings.SECRET_KEY, base)).hexdigest()[:14]


def loads(dry):
    checksum = dry[:14]
    base = dry[14:]

    if _checksum(base) == checksum:
        return pickle.loads(base64.decodestring(base))
    else:
        raise ValueError("pickle checksum is invalid")


def dumps(wet):
    base = base64.encodestring(pickle.dumps(wet, pickle.HIGHEST_PROTOCOL))
    checksum = _checksum(base)
    return '%s%s' % (checksum, base)
