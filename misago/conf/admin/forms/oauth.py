from django import forms
from django.utils.translation import gettext_lazy as _

from ....admin.forms import YesNoSwitch
from .base import ChangeSettingsForm


class ChangeOAuthSettingsForm(ChangeSettingsForm):
    settings = [
        "enable_oauth2_client",
        "oauth2_client_id",
        "oauth2_client_secret",
        "oauth2_scopes",
        "oauth2_login_url",
        "oauth2_token_url",
        "oauth2_token_method",
        "oauth2_json_token_path",
        "oauth2_user_url",
        "oauth2_user_method",
        "oauth2_user_auth_location",
        "oauth2_user_auth_name",
        "oauth2_json_id_path",
        "oauth2_json_name_path",
        "oauth2_json_email_path",
        "oauth2_json_avatar_path",
    ]

    enable_oauth2_client = YesNoSwitch(
        label=_("Enable OAuth Client"),
        help_text=_(
            "Enabling OAuth client will make login option redirect users to the OAuth provider "
            "configured below. It will also disable option to register on forum, "
            "change username, email or password, as those features will be delegated "
            "to the 3rd party site."
        ),
    )
    oauth2_client_id = forms.CharField(
        label=_("Client ID"),
        max_length=200,
        required=False,
    )
    oauth2_client_secret = forms.CharField(
        label=_("Client Secret"),
        max_length=200,
        required=False,
    )
    oauth2_scopes = forms.CharField(
        label=_("Scopes"),
        help_text=_("List of scopes to request from provider, separated with spaces."),
        max_length=500,
        required=False,
    )

    oauth2_login_url = forms.URLField(
        label=_("Login form URL"),
        help_text=_(
            "Address to login form on provider's server that users will be "
            "redirected to."
        ),
        max_length=500,
        required=False,
    )

    oauth2_token_url = forms.URLField(
        label=_("Access token retrieval URL"),
        help_text=_(
            "URL that will be called after user completes the login process "
            "and authorization code is sent back to your site. This URL "
            "is expected to take this code and return access token."
        ),
        max_length=500,
        required=False,
    )
    oauth2_token_method = forms.ChoiceField(
        label=_("Request method"),
        choices=[
            ("POST", "POST"),
            ("GET", "GET"),
        ],
        widget=forms.RadioSelect(),
    )
    oauth2_json_token_path = forms.CharField(
        label=_("JSON path to authorization token"),
        max_length=500,
        required=False,
    )

    oauth2_user_url = forms.URLField(
        label=_("User URL"),
        max_length=500,
        required=False,
    )
    oauth2_user_method = forms.ChoiceField(
        label=_("Request method"),
        choices=[
            ("POST", "POST"),
            ("GET", "GET"),
        ],
        widget=forms.RadioSelect(),
    )
    oauth2_user_auth_location = forms.ChoiceField(
        label=_("Authorization location"),
        choices=[
            ("HEADER", _("HTTP header")),
            ("QUERY", _("Query string")),
        ],
        widget=forms.RadioSelect(),
    )
    oauth2_user_auth_name = forms.CharField(
        label=_("Authorization variable"),
        max_length=200,
        required=False,
    )

    oauth2_json_id_path = forms.CharField(
        label=_("User ID path"),
        max_length=200,
        required=False,
    )
    oauth2_json_name_path = forms.CharField(
        label=_("User name path"),
        max_length=200,
        required=False,
    )
    oauth2_json_email_path = forms.CharField(
        label=_("User e-mail path"),
        max_length=200,
        required=False,
    )
    oauth2_json_avatar_path = forms.CharField(
        label=_("User avatar path"),
        max_length=200,
        required=False,
    )

    def clean_scopes(self):
        scopes = set(
            [
                scope.trim()
                for scope in self.cleaned_data["scopes"].split(" ")
                if scope.trim()
            ]
        )

        return " ".join(scopes) or None
