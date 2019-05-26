from django import forms
from django.utils.translation import gettext_lazy as _

from ....admin.forms import YesNoSwitch
from .base import ChangeSettingsForm


class ChangeThreadsSettingsForm(ChangeSettingsForm):
    settings = [
        "post_length_max",
        "post_length_min",
        "thread_title_length_max",
        "thread_title_length_min",
    ]

    post_length_max = forms.IntegerField(
        label=_("Maximum allowed post length"), min_value=0
    )
    post_length_min = forms.IntegerField(
        label=_("Minimum required post length"), min_value=1
    )
    thread_title_length_max = forms.IntegerField(
        label=_("Maximum allowed thread title length"), min_value=2, max_value=255
    )
    thread_title_length_min = forms.IntegerField(
        label=_("Minimum required thread title length"), min_value=2, max_value=255
    )
