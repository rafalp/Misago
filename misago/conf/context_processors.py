from django.templatetags.static import static
from django.urls import reverse
from django.utils.translation import get_language

from . import settings


def conf(request):
    return {
        "BLANK_AVATAR_URL": (
            request.settings.blank_avatar or static(settings.MISAGO_BLANK_AVATAR)
        ),
        "DEBUG": settings.DEBUG,
        "LANGUAGE_CODE_SHORT": get_language()[:2],
        "LOGIN_REDIRECT_URL": settings.LOGIN_REDIRECT_URL,
        "LOGIN_URL": settings.LOGIN_URL,
        "LOGOUT_URL": settings.LOGOUT_URL,
        "THREADS_ON_INDEX": settings.MISAGO_THREADS_ON_INDEX,
        "settings": request.settings,
    }


def og_image(request):
    og_image = request.settings.get("og_image")
    if not og_image["value"]:
        return {"og_image": None}

    return {
        "og_image": {
            "url": og_image["value"],
            "width": og_image["width"],
            "height": og_image["height"],
        }
    }


def preload_settings_json(request):
    preloaded_settings = request.settings.get_public_settings()

    preloaded_settings.update(
        {
            "LOGIN_API_URL": settings.MISAGO_LOGIN_API_URL,
            "LOGIN_REDIRECT_URL": reverse(settings.LOGIN_REDIRECT_URL),
            "LOGIN_URL": reverse(settings.LOGIN_URL),
            "LOGOUT_URL": reverse(settings.LOGOUT_URL),
        }
    )

    request.frontend_context.update(
        {
            "BLANK_AVATAR_URL": (
                request.settings.blank_avatar or static(settings.MISAGO_BLANK_AVATAR)
            ),
            "CSRF_COOKIE_NAME": settings.CSRF_COOKIE_NAME,
            "ENABLE_DELETE_OWN_ACCOUNT": request.settings.allow_delete_own_account,
            "ENABLE_DOWNLOAD_OWN_DATA": request.settings.allow_data_downloads,
            "MISAGO_PATH": reverse("misago:index"),
            "SETTINGS": preloaded_settings,
            "STATIC_URL": settings.STATIC_URL,
            "THREADS_ON_INDEX": settings.MISAGO_THREADS_ON_INDEX,
        }
    )

    return {}
