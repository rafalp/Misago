from hashlib import md5

from django.conf import settings


def hash_trigger(message):
    return md5('%s:%s' % (message, settings.SECRET_KEY)).hexdigest()[:8]


def variables_dict(plain=None, links=None, users=None, threads=None):
    final_variables = {}

    final_variables.update(plain)

    return final_variables
