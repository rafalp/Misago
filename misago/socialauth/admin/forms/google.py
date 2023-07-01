from django import forms
from django.utils.translation import pgettext_lazy

from .base import OAuthProviderForm


class GoogleForm(OAuthProviderForm):
    key = forms.CharField(
        label=pgettext_lazy("admin social auth google form", "Client ID"),
        required=False,
    )
    secret = forms.CharField(
        label=pgettext_lazy("admin social auth google form", "Client Secret"),
        required=False,
    )
