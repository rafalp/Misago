from django import forms
from django.utils.translation import pgettext_lazy

from .base import OAuthProviderForm


class GitHubForm(OAuthProviderForm):
    key = forms.CharField(
        label=pgettext_lazy("admin social auth github form", "Client ID"),
        required=False,
    )
    secret = forms.CharField(
        label=pgettext_lazy("admin social auth github form", "Client Secret"),
        required=False,
    )
