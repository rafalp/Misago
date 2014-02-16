from misago.core import threadstore


CACHE_KEY = 'misago_db_settings'


class DBSettings(object):
    def __init__(self):
        self._settings = self._read_cache()

    def _read_cache(self):
        from misago.core.cache import cache

        data = cache.get(CACHE_KEY, 'nada')
        if data == 'nada':
            data = self._read_db()
            cache.set(CACHE_KEY, data)
        return data

    def _read_db(self):
        from misago.conf.models import Setting

        data = {}
        for setting in Setting.objects.iterator():
            if setting.is_lazy:
                data[setting.setting] = {
                    'value': True if setting.value else False,
                    'is_lazy': setting.is_lazy
                }
            else:
                data[setting.setting] = {
                    'value': setting.value,
                    'is_lazy': setting.is_lazy
                }
        return data

    def get_lazy_setting(self, setting):
        from misago.conf.models import Setting

        try:
            if self._settings[setting]['is_lazy']:
                return Setting.objects.get(setting=setting).value
            else:
                raise ValueError("Setting %s is not lazy" % setting)
        except (KeyError, Setting.DoesNotExist):
            raise AttributeError("Setting %s is undefined" % setting)

    def __getattr__(self, attr):
        try:
            return self._settings[attr]['value']
        except KeyError:
            raise AttributeError("Setting %s is undefined" % attr)


class _DBSettingsGateway(object):
    def get_db_settings(self):
        dbsettings = threadstore.get(CACHE_KEY)
        if not dbsettings:
            dbsettings = DBSettings()
            threadstore.set(CACHE_KEY, dbsettings)
        return dbsettings

    def __getattr__(self, attr):
        return getattr(self.get_db_settings(), attr)


db_settings = _DBSettingsGateway()
