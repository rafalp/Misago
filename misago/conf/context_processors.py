from django.conf import settings
from misago.conf.dbsettings import db_settings


def settings(request):
    return {
        'misago_settings': db_settings,
        'LOGIN_REDIRECT_URL': 'misago:index',
        'LOGIN_URL': 'misago:login',
        'LOGOUT_URL': 'misago:logout',
    }
