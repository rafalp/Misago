from django.urls import reverse
from social_core.backends.utils import load_backends
from unidecode import unidecode

from misago.conf import settings

from .backendsnames import BACKENDS_NAMES


def get_enabled_social_auth_sites_list():
    social_auth_backends = load_backends(settings.AUTHENTICATION_BACKENDS)
    providers_list = []
    for backend_id in social_auth_backends:
        backend_name = get_social_auth_backend_name(backend_id)
            
        providers_list.append({
            'id': backend_id,
            'name': backend_name,
            'url': reverse('social:begin', kwargs={'backend': backend_id}),
        })
    return providers_list


def get_social_auth_backend_name(backend_id):
    if backend_id in settings.MISAGO_SOCIAL_AUTH_BACKENDS_NAMES:
        return settings.MISAGO_SOCIAL_AUTH_BACKENDS_NAMES[backend_id]
    if backend_id in BACKENDS_NAMES:
        return BACKENDS_NAMES[backend_id]
    return backend_id.title()


def perpare_username(username):
    return ''.join(filter(str.isalnum, unidecode(username)))