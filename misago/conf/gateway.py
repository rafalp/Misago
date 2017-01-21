from django.conf import settings as dj_settings

from . import defaults
from .dbsettings import db_settings


class SettingsGateway(object):
    def __getattr__(self, name):
        try:
            return getattr(dj_settings, name)
        except AttributeError:
            pass

        try:
            return getattr(defaults, name)
        except AttributeError:
            pass

        return getattr(db_settings, name)


settings = SettingsGateway()
