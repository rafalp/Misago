"""
Changed credentials service

Stores new e-mail and password in cache
"""
from hashlib import sha256

from misago.conf import settings
from misago.core.cache import cache
from misago.users import tokens


__all__ = ['cache_new_credentials', 'get_new_credentials']


TOKEN_NAME = 'new_credentials'
CACHE_PATTERN = 'new_credentials_%s'
CACHE_TIMEOUT = 3600 * 48


def cache_new_credentials(user, new_email, new_password):
    new_credentials = {
        'user_pk': user.pk,
        'email': new_email,
        'email_checksum': _make_checksum(user, new_email),
        'password': new_password,
        'password_checksum': _make_checksum(user, new_password),
    }

    cache.set(_make_cache_name(user), new_credentials, CACHE_TIMEOUT)
    return _make_token(user)


def get_new_credentials(user, token):
    if token != _make_token(user):
        return None

    new_credentials = cache.get(_make_cache_name(user), 'nada')

    if new_credentials == 'nada':
        raise Exception('CACHE NOT FOUND')
        return None

    if new_credentials['user_pk'] != user.pk:
        return None

    email_checksum = _make_checksum(user, new_credentials['email'])
    if new_credentials['email_checksum'] != email_checksum:
        raise Exception('MAIL CHECKSUM FAIL')
        return None

    password_checksum = _make_checksum(user, new_credentials['password'])
    if new_credentials['password_checksum'] != password_checksum:
        raise Exception('PASS CHECKSUM FAIL')
        return None

    return new_credentials


def _make_token(user):
    return tokens.make(user, TOKEN_NAME)


def _make_cache_name(user):
    return CACHE_PATTERN % _make_token(user)


def _make_checksum(user, value):
    seeds = (
        user.pk,
        user.email,
        user.password,
        user.last_login.replace(microsecond=0, tzinfo=None),
        settings.SECRET_KEY,
        unicode(value)
    )

    return sha256('+'.join([unicode(s) for s in seeds])).hexdigest()
