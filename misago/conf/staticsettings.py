from django.conf import settings

from . import defaults


class StaticSettings:
    def __getattr__(self, name):
        try:
            return getattr(settings, name)
        except AttributeError:
            pass

        try:
            return getattr(defaults, name)
        except AttributeError:
            pass

        raise AttributeError("%s setting is not defined" % name)
