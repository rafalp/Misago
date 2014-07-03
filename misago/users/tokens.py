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


def is_valid(token, user, token_type):
    return token == make(user, token_type)
