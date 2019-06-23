from django import forms
from django.utils.translation import gettext_lazy as _

from .base import ProviderForm


class FacebookForm(ProviderForm):
    key = forms.CharField(label=_("App ID"))
    secret = forms.CharField(label=_("App Secret"))
