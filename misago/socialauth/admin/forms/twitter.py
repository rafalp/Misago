from django import forms
from django.utils.translation import gettext_lazy as _

from .base import OAuthProviderForm


class TwitterForm(OAuthProviderForm):
    key = forms.CharField(label=_("Consumer API key"), required=False)
    secret = forms.CharField(label=_("Consumer API secret key"), required=False)
