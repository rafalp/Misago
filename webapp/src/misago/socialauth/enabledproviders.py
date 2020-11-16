from .cache import get_socialauth_cache, set_socialauth_cache
from .models import SocialAuthProvider
from .providers import providers


def get_enabled_providers(cache_versions):
    data = get_socialauth_cache(cache_versions)
    if data is None:
        data = get_providers_from_db()
        set_socialauth_cache(cache_versions, data)
    for provider, options in data.items():
        options["auth_backend"] = providers.get_auth_backend(provider)
    return data


def get_providers_from_db():
    data = {}
    for provider in SocialAuthProvider.objects.filter(is_active=True):
        data[provider.pk] = {
            "pk": provider.pk,
            "name": providers.get_name(provider.pk),
            "settings": get_provider_settings(provider),
            "auth_backend": None,
            "button_text": provider.button_text,
            "button_color": provider.button_color,
        }
    return data


def get_provider_settings(provider):
    settings = {}
    if providers.get_settings(provider.pk):
        for key, value in providers.get_settings(provider.pk).items():
            settings[key.upper()] = value
    if provider.settings:
        for key, value in provider.settings.items():
            settings[key.upper()] = value
    return settings
