from django import forms

from ..cache import clear_settings_cache


class ChangeSettingsForm(forms.Form):
    settings = []

    def save(self, settings):
        self.save_settings(settings)
        self.clear_cache()

    def save_settings(self, settings):
        for setting in self.settings:
            setting_obj = settings[setting]
            new_value = self.cleaned_data.get(setting)
            self.save_setting(setting_obj, new_value)

    def save_setting(self, setting, value):
        setting.value = value
        setting.save()

    def clear_cache(self):
        clear_settings_cache()
