from django.templatetags.static import static
from django.urls import reverse
from django.utils.translation import get_language

from . import settings
from ..users.social.utils import get_enabled_social_auth_sites_list

BLANK_AVATAR_URL = static(settings.MISAGO_BLANK_AVATAR)


def conf(request):
    return {
        "BLANK_AVATAR_URL": BLANK_AVATAR_URL,
        "DEBUG": settings.DEBUG,
        "LANGUAGE_CODE_SHORT": get_language()[:2],
        "LOGIN_REDIRECT_URL": settings.LOGIN_REDIRECT_URL,
        "LOGIN_URL": settings.LOGIN_URL,
        "LOGOUT_URL": settings.LOGOUT_URL,
        "THREADS_ON_INDEX": settings.MISAGO_THREADS_ON_INDEX,
        "settings": request.settings,
    }


def preload_settings_json(request):
    preloaded_settings = request.settings.get_public_settings()

    preloaded_settings.update(
        {
            "LOGIN_API_URL": settings.MISAGO_LOGIN_API_URL,
            "LOGIN_REDIRECT_URL": reverse(settings.LOGIN_REDIRECT_URL),
            "LOGIN_URL": reverse(settings.LOGIN_URL),
            "LOGOUT_URL": reverse(settings.LOGOUT_URL),
            "SOCIAL_AUTH": get_enabled_social_auth_sites_list(),
        }
    )

    request.frontend_context.update(
        {
            "BLANK_AVATAR_URL": BLANK_AVATAR_URL,
            "CSRF_COOKIE_NAME": settings.CSRF_COOKIE_NAME,
            "ENABLE_DELETE_OWN_ACCOUNT": settings.MISAGO_ENABLE_DELETE_OWN_ACCOUNT,
            "ENABLE_DOWNLOAD_OWN_DATA": settings.MISAGO_ENABLE_DOWNLOAD_OWN_DATA,
            "MISAGO_PATH": reverse("misago:index"),
            "SETTINGS": preloaded_settings,
            "STATIC_URL": settings.STATIC_URL,
            "THREADS_ON_INDEX": settings.MISAGO_THREADS_ON_INDEX,
        }
    )

    return {}
