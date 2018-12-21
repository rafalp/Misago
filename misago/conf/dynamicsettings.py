from .cache import get_settings_cache, set_settings_cache
from .models import Setting


class DynamicSettings:
    _overrides = {}

    def __init__(self, cache_versions):
        self._settings = get_settings_cache(cache_versions)
        if self._settings is None:
            self._settings = get_settings_from_db()
            set_settings_cache(cache_versions, self._settings)

    def get_public_settings(self):
        public_settings = {}
        for name, setting in self._settings.items():
            if setting["is_public"]:
                public_settings[name] = setting["value"]
        return public_settings

    def get_lazy_setting_value(self, setting):
        try:
            if self._settings[setting]["is_lazy"]:
                if setting in self._overrides:
                    return self._overrides[setting]
                if not self._settings[setting].get("real_value"):
                    real_value = Setting.objects.get(setting=setting).value
                    self._settings[setting]["real_value"] = real_value
                return self._settings[setting]["real_value"]
            raise ValueError("Setting %s is not lazy" % setting)
        except (KeyError, Setting.DoesNotExist):
            raise AttributeError("Setting %s is not defined" % setting)

    def __getattr__(self, setting):
        if setting in self._overrides:
            return self._overrides[setting]
        if setting in self._settings:
            return self._settings[setting]["value"]
        raise AttributeError("Setting %s is not defined" % setting)

    @classmethod
    def override_settings(cls, overrides):
        cls._overrides = overrides

    @classmethod
    def remove_overrides(cls):
        cls._overrides = {}


def get_settings_from_db():
    settings = {}
    for setting in Setting.objects.iterator():
        if setting.is_lazy:
            settings[setting.setting] = {
                'value': True if setting.value else None,
                'is_lazy': setting.is_lazy,
                'is_public': setting.is_public,
            }
        else:
            settings[setting.setting] = {
                'value': setting.value,
                'is_lazy': setting.is_lazy,
                'is_public': setting.is_public,
            }
    return settings
