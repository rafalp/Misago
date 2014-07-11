from hashlib import sha256

from django.conf import settings


def make(user, token_type):
    seeds = (
        user.pk,
        user.email,
        user.password,
        user.last_login.replace(microsecond=0, tzinfo=None),
        token_type,
        settings.SECRET_KEY,
    )

    return sha256('+'.join([unicode(s) for s in seeds])).hexdigest()[:12]


def is_valid(user, token_type, token):
    return token == make(user, token_type)


"""
Shortcuts for activation token
"""
ACTIVATION_TOKEN = 'activation'


def make_activation_token(user):
    return make(user, ACTIVATION_TOKEN)


def is_activation_token_valid(user, token):
    return is_valid(user, ACTIVATION_TOKEN, token)
