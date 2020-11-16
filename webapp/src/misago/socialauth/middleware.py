from django.utils.functional import SimpleLazyObject

from .enabledproviders import get_enabled_providers


def socialauth_providers_middleware(get_response):
    """Sets request.socialauth attribute with dict of setup social auth providers."""

    def middleware(request):
        def lazily_get_enabled_providers():
            return get_enabled_providers(request.cache_versions)

        request.socialauth = SimpleLazyObject(lazily_get_enabled_providers)
        return get_response(request)

    return middleware
