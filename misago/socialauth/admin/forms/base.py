from django import forms
from django.utils.translation import gettext_lazy as _

from ....admin.forms import YesNoSwitch
from ...models import SocialAuthProvider
from ..ordering import get_next_free_order


class ProviderForm(forms.ModelForm):
    button_text = forms.CharField(label=_("Button text"), required=False)
    button_color = forms.CharField(label=_("Button color"), required=False)
    is_active = YesNoSwitch(label=_("Enable this provider"))

    class Meta:
        model = SocialAuthProvider
        fields = ["button_text", "button_color", "is_active"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def save(self):
        settings = {}
        for setting, value in self.cleaned_data.items():
            if setting not in ["button_text", "button_color", "is_active"]:
                settings[setting] = value
        self.instance.settings = settings

        if "is_active" in self.changed_data and self.cleaned_data.get("is_active"):
            self.instance.order = get_next_free_order()

        self.instance.save()
