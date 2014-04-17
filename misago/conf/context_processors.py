from django.conf import settings as dj_settings
from misago.conf.dbsettings import db_settings


def settings(request):
    return {
        'misago_settings': db_settings,
        'LOGIN_REDIRECT_URL': dj_settings.LOGIN_REDIRECT_URL,
        'LOGIN_URL': dj_settings.LOGIN_URL,
        'LOGOUT_URL': dj_settings.LOGOUT_URL,
    }
