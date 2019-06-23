from django import forms
from django.utils.translation import gettext_lazy as _

from .base import ProviderForm


class TwitterForm(ProviderForm):
    key = forms.CharField(label=_("Consumer API key"))
    secret = forms.CharField(label=_("Consumer API secret key"))
