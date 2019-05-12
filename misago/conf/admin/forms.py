from django import forms

from ..cache import clear_settings_cache


class ChangeSettingsForm(forms.Form):
    settings = []
    files = []

    def save(self, settings_dict):
        self.save_settings(settings_dict)
        self.clear_cache()

    def save_settings(self, settings_dict):
        for setting in self.settings:
            setting_obj = settings_dict.get(setting)
            if not setting_obj:
                raise ValueError(
                    "ChangeSettingsForm.save() was called with dict that was missing "
                    "setting instance for %s" % setting
                )
            self.save_setting(setting_obj, self.cleaned_data.get(setting))

    def save_setting(self, setting, value):
        setting.value = value
        setting.save()

    def clear_cache(self):
        clear_settings_cache()
