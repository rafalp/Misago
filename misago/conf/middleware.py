from django.utils.functional import SimpleLazyObject

from .dynamicsettings import DynamicSettings


def dynamic_settings_middleware(get_response):
    """Sets request.settings attribute with DynamicSettings."""

    def middleware(request):
        def get_dynamic_settings():
            return DynamicSettings(request.cache_versions)

        request.settings = SimpleLazyObject(get_dynamic_settings)
        return get_response(request)

    return middleware
