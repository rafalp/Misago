"""
Token creation

Token is base encoded string containing three values:

- days since unix epoch (so we can validate token expiration)
- hash unique for current state of user model
- token checksum for discovering manipulations
"""
import base64
from hashlib import sha256
from time import time

from django.conf import settings
from django.utils.encoding import force_bytes


def make(user, token_type):
    user_hash = _make_hash(user, token_type)
    creation_day = _days_since_epoch()

    obfuscated = base64.b64encode(
        force_bytes("%s%s" % (user_hash, creation_day))
    ).decode()
    obfuscated = obfuscated.rstrip("=")
    checksum = _make_checksum(obfuscated)

    return "%s%s" % (checksum, obfuscated)


def is_valid(user, token_type, token):
    checksum = token[:8]
    obfuscated = token[8:]

    if checksum != _make_checksum(obfuscated):
        return False

    unobfuscated = base64.b64decode(obfuscated + "=" * (-len(obfuscated) % 4)).decode()
    user_hash = unobfuscated[:8]

    if user_hash != _make_hash(user, token_type):
        return False

    creation_day = int(unobfuscated[8:])
    return creation_day + 5 >= _days_since_epoch()


def _make_hash(user, token_type):
    seeds = [
        user.pk,
        user.email,
        user.password,
        user.last_login.replace(microsecond=0, tzinfo=None),
        token_type,
        settings.SECRET_KEY,
    ]

    return sha256(force_bytes("+".join([str(s) for s in seeds]))).hexdigest()[:8]


def _days_since_epoch():
    return int(time() / (25 * 3600))


def _make_checksum(obfuscated):
    return sha256(force_bytes("%s:%s" % (settings.SECRET_KEY, obfuscated))).hexdigest()[
        :8
    ]


ACTIVATION_TOKEN = "activation"


def make_activation_token(user):
    return make(user, ACTIVATION_TOKEN)


def is_activation_token_valid(user, token):
    return is_valid(user, ACTIVATION_TOKEN, token)


PASSWORD_CHANGE_TOKEN = "change_password"


def make_password_change_token(user):
    return make(user, PASSWORD_CHANGE_TOKEN)


def is_password_change_token_valid(user, token):
    return is_valid(user, PASSWORD_CHANGE_TOKEN, token)
