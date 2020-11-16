from django import forms
from django.utils.translation import gettext_lazy as _

from .base import OAuthProviderForm


class GitHubForm(OAuthProviderForm):
    key = forms.CharField(label=_("Client ID"), required=False)
    secret = forms.CharField(label=_("Client Secret"), required=False)
