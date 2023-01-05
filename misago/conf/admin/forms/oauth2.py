from django import forms
from django.contrib import messages
from django.utils.translation import gettext, gettext_lazy as _

from ....admin.forms import YesNoSwitch
from .base import ChangeSettingsForm


class ChangeOAuth2SettingsForm(ChangeSettingsForm):
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
        "oauth2_user_token_location",
        "oauth2_user_token_name",
        "oauth2_json_id_path",
        "oauth2_json_name_path",
        "oauth2_json_email_path",
        "oauth2_json_avatar_path",
    ]

    enable_oauth2_client = YesNoSwitch(
        label=_("Enable OAuth2 client"),
        help_text=_(
            "Enabling OAuth2 will make login option redirect users to the OAuth provider "
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
            "is expected to take this code and return the access token that "
            "will be next used to retrieve user data."
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
        label=_("JSON path to access token"),
        help_text=_(
            "Name of key containing the access token in JSON returned by the provider "
            'If token is nested, use period (".") for path, eg: "result.token" '
            'will retrieve the token from "token" key nested in "result".'
        ),
        max_length=500,
        required=False,
    )

    oauth2_user_url = forms.URLField(
        label=_("User data URL"),
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
    oauth2_user_token_location = forms.ChoiceField(
        label=_("Access token location"),
        choices=[
            ("HEADER", _("HTTP header")),
            ("QUERY", _("Query string")),
        ],
        widget=forms.RadioSelect(),
    )
    oauth2_user_token_name = forms.CharField(
        label=_("Access token name"),
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
        label=_("User avatar URL path"),
        help_text=_("Optional, leave empty to don't download avatar from provider."),
        max_length=200,
        required=False,
    )

    def clean_oauth2_scopes(self):
        # Remove duplicates and extra spaces, keep order of scopes
        clean_scopes = []
        for scope in self.cleaned_data["oauth2_scopes"].split():
            scope = scope.strip()
            if scope and scope not in clean_scopes:
                clean_scopes.append(scope)

        return " ".join(clean_scopes) or None

    def clean(self):
        data = super().clean()

        if not data.get("enable_oauth2_client"):
            return data

        required_data = [data[key] for key in data if key != "oauth2_json_avatar_path"]

        if not all(required_data):
            data["enable_oauth2_client"] = False

            messages.error(
                self.request,
                gettext(
                    "You need to complete the configuration before you will be able to "
                    "enable OAuth 2 on your site."
                ),
            )

        return data
