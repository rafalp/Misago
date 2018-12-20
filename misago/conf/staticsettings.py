from django.conf import settings

from . import defaults


class StaticSettings(object):
    def __getattr__(self, name):
        if name.lower() == name:
            raise Exception("Trying to access dynamic setting: %s" % name)

        try:
            return getattr(settings, name)
        except AttributeError:
            pass

        try:
            return getattr(defaults, name)
        except AttributeError:
            pass

        raise AttributeError
