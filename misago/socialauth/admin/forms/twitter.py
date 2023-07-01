from django import forms
from django.utils.translation import pgettext_lazy

from .base import OAuthProviderForm


class TwitterForm(OAuthProviderForm):
    key = forms.CharField(
        label=pgettext_lazy("admin social auth twitter form", "Consumer API key"),
        required=False,
    )
    secret = forms.CharField(
        label=pgettext_lazy(
            "admin social auth twitter form", "Consumer API secret key"
        ),
        required=False,
    )
