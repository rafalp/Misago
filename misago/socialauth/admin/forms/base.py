from django import forms
from django.utils.translation import gettext, pgettext_lazy

from ....admin.forms import ColorField, YesNoSwitch
from ...models import SocialAuthProvider
from ..ordering import get_next_free_order


class ProviderForm(forms.ModelForm):
    button_text = forms.CharField(
        label=pgettext_lazy("admin social auth provider form", "Button text"),
        required=False,
    )
    button_color = ColorField(
        label=pgettext_lazy("admin social auth provider form", "Button color"),
        required=False,
    )
    is_active = YesNoSwitch(
        label=pgettext_lazy("admin social auth provider form", "Enable this provider")
    )

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


class OAuthProviderForm(ProviderForm):
    associate_by_email = YesNoSwitch(
        label=pgettext_lazy(
            "admin social auth provider form", "Associate existing users by email"
        ),
        help_text=pgettext_lazy(
            "admin social auth provider form",
            "This setting controls handling of e-mail collisions that occur when e-mail address returned from social site is already stored in the forum's database. Enabling this option will result in the user being signed in to pre-existing account. Otherwise they will be asked to specify a different e-mail to complete the sign in using social site.",
        ),
    )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("is_active"):
            if not cleaned_data.get("key"):
                self.add_error("key", gettext("This field is required."))
            if not cleaned_data.get("secret"):
                self.add_error("secret", gettext("This field is required."))

        return cleaned_data
