import json

from django.core.urlresolvers import reverse
from misago.conf.gateway import dj_settings, db_settings  # noqa


def settings(request):
    return {
        'DEBUG': dj_settings.DEBUG,
        'misago_settings': db_settings,

        'LOGIN_REDIRECT_URL': dj_settings.LOGIN_REDIRECT_URL,
        'LOGIN_URL': dj_settings.LOGIN_URL,
        'LOGOUT_URL': dj_settings.LOGOUT_URL,
    }


def preload_config_json(request):
    preloaded_settings = db_settings.get_public_settings()

    preloaded_settings.update({
        'loginApiUrl': dj_settings.MISAGO_LOGIN_API_URL,

        'loginRedirectUrl': reverse(dj_settings.LOGIN_REDIRECT_URL),
        'loginUrl': reverse(dj_settings.LOGIN_URL),

        'logoutUrl': reverse(dj_settings.LOGOUT_URL),
    })

    request.preloaded_ember_data.update({
        'misagoSettings': preloaded_settings,

        'staticUrl': dj_settings.STATIC_URL,
        'mediaUrl': dj_settings.MEDIA_URL,

        'csrfCookieName': dj_settings.CSRF_COOKIE_NAME,
    })

    return {}
