"""
Changed credentials service

Stores new e-mail and password in cache
"""
from hashlib import sha256

from django.conf import settings
from django.utils import six
from django.utils.encoding import force_bytes


def store_new_credential(request, credential_type, credential_value):
    credential_key = 'new_credential_%s' % credential_type
    token = _make_change_token(request.user, credential_type)

    request.session[credential_key] = {
        'user_pk': request.user.pk,
        'credential': credential_value,
        'token': token,
    }

    return token


def read_new_credential(request, credential_type, link_token):
    try:
        credential_key = 'new_credential_%s' % credential_type
        new_credential = request.session.pop(credential_key)
    except KeyError:
        return None

    if new_credential['user_pk'] != request.user.pk:
        return None

    current_token = _make_change_token(request.user, credential_type)
    if link_token != current_token:
        return None
    if new_credential['token'] != current_token:
        return None

    return new_credential['credential']


def _make_change_token(user, token_type):
    seeds = (
        user.pk, user.email, user.password, user.last_login.replace(microsecond=0, tzinfo=None),
        settings.SECRET_KEY, six.text_type(token_type)
    )

    return sha256(force_bytes('+'.join([six.text_type(s) for s in seeds]))).hexdigest()
