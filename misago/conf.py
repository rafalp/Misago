from django.conf import settings as dj_settings
from django.core.cache import cache
from misago.models import Setting
from misago.thread import local

_thread_local = local()

def load_settings():
    settings = cache.get('settings', {})
    if not settings:
        for i in Setting.objects.all():
            settings[i.pk] = i.value
        cache.set('settings', settings)
    return settings


class MisagoSettings(object):
    def __init__(self, local, safe):
        self.thread = local
        self.is_safe = safe

    def settings(self):
        try:
            return self.thread.settings
        except AttributeError:
            self.thread.settings = load_settings()
            return self.thread.settings

    def setting(self, key):
        try:
            try:
                return self.settings()[key]
            except KeyError:
                if self.is_safe:
                    return getattr(dj_settings, key)
                else:
                    raise AttributeError()
        except AttributeError:
            raise Exception(u"Requested setting \"%s\" could not be found." % key)

    def __contains__(self, key):
        return key in self.settings()

    def __getitem__(self, key):
        return self.setting(key)

    def __getattr__(self, key):
        return self.setting(key)

    def __setitem__(self, key, value):
        setting = Setting.objects.get(pk=key)
        setting.value = value
        setting.save(force_update=True)


settings = MisagoSettings(_thread_local, True)


def SafeSettings():
    """
    Safe settings factory for MisagoSettings
    """
    return MisagoSettings(_thread_local, False)