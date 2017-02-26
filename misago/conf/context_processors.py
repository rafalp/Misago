from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse
from django.utils.translation import get_language

from .gateway import settings as misago_settings  # noqa
from .gateway import db_settings


BLANK_AVATAR_URL = static(misago_settings.MISAGO_BLANK_AVATAR)


def settings(request):
    return {
        'DEBUG': misago_settings.DEBUG,
        'LANGUAGE_CODE_SHORT': get_language()[:2],
        'misago_settings': db_settings,
        'BLANK_AVATAR_URL': BLANK_AVATAR_URL,
        'THREADS_ON_INDEX': misago_settings.MISAGO_THREADS_ON_INDEX,
        'LOGIN_REDIRECT_URL': misago_settings.LOGIN_REDIRECT_URL,
        'LOGIN_URL': misago_settings.LOGIN_URL,
        'LOGOUT_URL': misago_settings.LOGOUT_URL,
    }


def preload_settings_json(request):
    preloaded_settings = db_settings.get_public_settings()

    preloaded_settings.update({
        'LOGIN_API_URL': misago_settings.MISAGO_LOGIN_API_URL,
        'LOGIN_REDIRECT_URL': reverse(misago_settings.LOGIN_REDIRECT_URL),
        'LOGIN_URL': reverse(misago_settings.LOGIN_URL),
        'LOGOUT_URL': reverse(misago_settings.LOGOUT_URL),
    })

    request.frontend_context.update({
        'SETTINGS': preloaded_settings,
        'MISAGO_PATH': reverse('misago:index'),
        'BLANK_AVATAR_URL': BLANK_AVATAR_URL,
        'STATIC_URL': misago_settings.STATIC_URL,
        'CSRF_COOKIE_NAME': misago_settings.CSRF_COOKIE_NAME,
        'THREADS_ON_INDEX': misago_settings.MISAGO_THREADS_ON_INDEX,
    })

    return {}
