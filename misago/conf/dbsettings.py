from misago.core import threadstore


CACHE_KEY = 'misago_db_settings'


class DBSettings(object):
    def __init__(self):
        self._settings = self._read_cache()
        self._overrides = {}

    def _read_cache(self):
        from misago.core.cache import cache

        data = cache.get(CACHE_KEY, 'nada')
        if data == 'nada':
            data = self._read_db()
            cache.set(CACHE_KEY, data)
        return data

    def _read_db(self):
        from .models import Setting

        data = {}
        for setting in Setting.objects.iterator():
            if setting.is_lazy:
                data[setting.setting] = {
                    'value': True if setting.value else None,
                    'is_lazy': setting.is_lazy,
                    'is_public': setting.is_public,
                }
            else:
                data[setting.setting] = {
                    'value': setting.value,
                    'is_lazy': setting.is_lazy,
                    'is_public': setting.is_public,
                }
        return data

    def get_public_settings(self):
        public_settings = {}
        for name, setting in self._settings.items():
            if setting['is_public']:
                public_settings[name] = setting['value']
        return public_settings

    def get_lazy_setting(self, setting):
        from .models import Setting

        try:
            if self._settings[setting]['is_lazy']:
                if not self._settings[setting].get('real_value'):
                    real_value = Setting.objects.get(setting=setting).value
                    self._settings[setting]['real_value'] = real_value
                return self._settings[setting]['real_value']
            else:
                raise ValueError("Setting %s is not lazy" % setting)
        except (KeyError, Setting.DoesNotExist):
            raise AttributeError("Setting %s is undefined" % setting)

    def flush_cache(self):
        from misago.core.cache import cache
        cache.delete(CACHE_KEY)

    def __getattr__(self, attr):
        try:
            return self._settings[attr]['value']
        except KeyError:
            raise AttributeError("Setting %s is undefined" % attr)

    def override_setting(self, setting, new_value):
        if not setting in self._overrides:
            self._overrides[setting] = self._settings[setting]['value']
        self._settings[setting]['value'] = new_value
        self._settings[setting]['real_value'] = new_value
        return new_value

    def reset_settings(self):
        for setting, original_value in self._overrides.items():
            self._settings[setting]['value'] = original_value
            self._settings[setting].pop('real_value', None)


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
