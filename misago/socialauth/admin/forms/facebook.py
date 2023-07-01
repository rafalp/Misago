from django import forms
from django.utils.translation import pgettext_lazy

from .base import OAuthProviderForm


class FacebookForm(OAuthProviderForm):
    key = forms.CharField(
        label=pgettext_lazy("admin social auth facebook form", "App ID"),
        required=False,
    )
    secret = forms.CharField(
        label=pgettext_lazy("admin social auth facebook form", "App Secret"),
        required=False,
    )
