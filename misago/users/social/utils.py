from social_core.backends.utils import load_backends

from misago.conf import settings

from .providersnames import PROVIDERS_NAMES


def get_enabled_social_auth_sites_list():
    social_auth_backends = load_backends(settings.AUTHENTICATION_BACKENDS)
    providers_list = []
    for provider_id in social_auth_backends:
        provider_name = settings.MISAGO_SOCIAL_AUTH_PROVIDERS_NAMES.get(provider_id)
        if not provider_name:
            provider_name = PROVIDERS_NAMES.get(provider_id, provider_id.title())
            
        providers_list.append({
            'id': provider_id,
            'name': provider_name,
        })
    return providers_list
