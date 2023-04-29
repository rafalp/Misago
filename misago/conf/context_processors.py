import json

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
        "CSRF_COOKIE_NAME": json.dumps(settings.CSRF_COOKIE_NAME),
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

    delegate_auth = request.settings.enable_oauth2_client

    if request.settings.enable_oauth2_client:
        login_url = reverse("misago:oauth2-login")
    else:
        login_url = reverse(settings.LOGIN_URL)

    preloaded_settings.update(
        {
            "DELEGATE_AUTH": delegate_auth,
            "LOGIN_API_URL": settings.MISAGO_LOGIN_API_URL,
            "LOGIN_REDIRECT_URL": reverse(settings.LOGIN_REDIRECT_URL),
            "LOGIN_URL": login_url,
            "LOGOUT_URL": reverse(settings.LOGOUT_URL),
        }
    )

    request.frontend_context.update(
        {
            "BLANK_AVATAR_URL": (
                request.settings.blank_avatar or static(settings.MISAGO_BLANK_AVATAR)
            ),
            "CSRF_COOKIE_NAME": settings.CSRF_COOKIE_NAME,
            "ENABLE_DELETE_OWN_ACCOUNT": (
                not delegate_auth and request.settings.allow_delete_own_account
            ),
            "ENABLE_DOWNLOAD_OWN_DATA": request.settings.allow_data_downloads,
            "MISAGO_PATH": reverse("misago:index"),
            "SETTINGS": preloaded_settings,
            "STATIC_URL": settings.STATIC_URL,
            "THREADS_ON_INDEX": settings.MISAGO_THREADS_ON_INDEX,
            "NOTIFICATIONS_API": reverse("misago:apiv2:notifications"),
            "NOTIFICATIONS_URL": reverse("misago:notifications"),
        }
    )

    if (
        request.user.is_authenticated
        and request.user.is_staff
        and request.settings.show_admin_panel_link_in_ui
    ):
        request.frontend_context["ADMIN_URL"] = reverse("misago:admin:index")

    return {}
