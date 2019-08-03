from django import forms
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from ....admin.forms import YesNoSwitch
from .base import ChangeSettingsForm


class ChangeSSOSettingsForm(ChangeSettingsForm):
    settings = ["enable_sso", "sso_public_key", "sso_private_key", "sso_url"]

    enable_sso = YesNoSwitch(
        label=_("Enable Single Sign-On"),
        help_text=_(
            "Enabling SSO will make login option redirect users to the server URL "
            "configured below. It will also disable option to register on forum, "
            "change username, email or passward, as those features will be delegated "
            "to the 3rd party site."
        ),
    )
    sso_public_key = forms.CharField(
        label=_("Public key"),
        help_text=_(
            "Leave this field empty for Misago to generate this key on form submission."
        ),
        max_length=64,
        required=False,
    )
    sso_private_key = forms.CharField(
        label=_("Private key"),
        help_text=_(
            "Leave this field empty for Misago to generate this key on form submission."
        ),
        max_length=64,
        required=False,
    )
    sso_url = forms.URLField(label=_("Server URL"), max_length=255, required=False)

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("enable_sso"):
            if not cleaned_data.get("sso_public_key"):
                cleaned_data["sso_public_key"] = get_random_string(64)
            if not cleaned_data.get("sso_private_key"):
                cleaned_data["sso_private_key"] = get_random_string(64)

            if not cleaned_data.get("sso_url"):
                self.add_error(
                    "sso_url", _("You need to enter server URL to enable SSO.")
                )

        return cleaned_data
