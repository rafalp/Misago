from .cache import get_settings_cache, set_settings_cache
from .models import Setting


class DynamicSettings:
    _overrides = {}

    def __init__(self, cache_versions):
        self._settings = get_settings_cache(cache_versions)
        if self._settings is None:
            self._settings = get_settings_from_db()
            set_settings_cache(cache_versions, self._settings)

    def get(self, setting):
        return self._settings.get(setting)

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
        settings[setting.setting] = {
            "value": None,
            "is_lazy": setting.is_lazy,
            "is_public": setting.is_public,
            "width": None,
            "height": None,
        }

        if setting.is_lazy:
            settings[setting.setting]["value"] = True if setting.value else None
        elif setting.python_type == "image":
            settings[setting.setting].update(
                {
                    "value": setting.value.url if setting.value else None,
                    "width": setting.image_width,
                    "height": setting.image_height,
                }
            )
        else:
            settings[setting.setting]["value"] = setting.value

    return settings
