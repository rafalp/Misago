from django import forms
from django.utils.translation import pgettext_lazy

from .base import OAuthProviderForm


class DiscordForm(OAuthProviderForm):
    key = forms.CharField(
        label=pgettext_lazy("admin social auth discord form", "App ID"),
        required=False,
    )
    secret = forms.CharField(
        label=pgettext_lazy("admin social auth discord form", "App Secret"),
        required=False,
    )
