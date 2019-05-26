from django import forms

from ...cache import clear_settings_cache


class ChangeSettingsForm(forms.Form):
    settings = []

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def save(self, settings):
        self.save_settings(settings)
        self.clear_cache()

    def save_settings(self, settings):
        for setting in self.settings:
            setting_obj = settings[setting]
            new_value = self.cleaned_data.get(setting)
            if setting_obj.python_type == "image":
                if new_value and new_value != self.initial.get(setting):
                    self.save_image(setting_obj, new_value)
                elif self.cleaned_data.get("%s_delete" % setting):
                    self.delete_image(setting_obj)
            else:
                self.save_setting(setting_obj, new_value)

    def delete_image(self, setting):
        if setting.image:
            setting.image.delete()

    def save_image(self, setting, value):
        if setting.image:
            setting.image.delete(save=False)
        setting.value = value
        setting.save()

    def save_setting(self, setting, value):
        setting.value = value
        setting.save()

    def clear_cache(self):
        clear_settings_cache()
