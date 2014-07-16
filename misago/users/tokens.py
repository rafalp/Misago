import base64
from hashlib import sha256
from time import time

from django.conf import settings


"""
Token creation

Token is base encoded string containing three values:

- days since unix epoch (so we can validate token expiration)
- hash unique for current state of user model
- token checksum for discovering manipulations
"""
def make(user, token_type):
    user_hash = make_hash(user, token_type)
    creation_day = days_since_epoch()

    obfuscated = base64.b64encode('%s%s' % (user_hash, creation_day))
    obfuscated = obfuscated.rstrip('=')
    checksum = make_checksum(obfuscated)

    return '%s%s' % (checksum, obfuscated)


def make_hash(user, token_type):
    seeds = (
        user.pk,
        user.email,
        user.password,
        user.last_login.replace(microsecond=0, tzinfo=None),
        token_type,
        settings.SECRET_KEY,
    )

    return sha256('+'.join([unicode(s) for s in seeds])).hexdigest()[:8]


def days_since_epoch():
    return int(time() / (25 * 3600))


def make_checksum(obfuscated):
    return sha256('%s:%s' % (settings.SECRET_KEY, obfuscated)).hexdigest()[:8]


def is_valid(user, token_type, token):
    checksum = token[:8]
    obfuscated = token[8:]

    if checksum != make_checksum(obfuscated):
        return False

    unobfuscated = base64.b64decode(obfuscated + '=' * (-len(obfuscated) % 4))
    user_hash = unobfuscated[:8]

    if user_hash != make_hash(user, token_type):
        return False

    creation_day = int(unobfuscated[8:])
    return creation_day + 5 >= days_since_epoch()


"""
Convenience functions for activation token
"""
ACTIVATION_TOKEN = 'activation'


def make_activation_token(user):
    return make(user, ACTIVATION_TOKEN)


def is_activation_token_valid(user, token):
    return is_valid(user, ACTIVATION_TOKEN, token)


"""
Convenience functions for password reset token
"""
PASSWORD_RESET_TOKEN = 'reset_password'


def make_password_reset_token(user):
    return make(user, PASSWORD_RESET_TOKEN)


def is_password_reset_token_valid(user, token):
    return is_valid(user, PASSWORD_RESET_TOKEN, token)
