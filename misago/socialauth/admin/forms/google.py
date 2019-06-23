from django import forms
from django.utils.translation import gettext_lazy as _

from .base import ProviderForm


class GoogleForm(ProviderForm):
    key = forms.CharField(label=_("Client ID"))
    secret = forms.CharField(label=_("Client Secret"))
