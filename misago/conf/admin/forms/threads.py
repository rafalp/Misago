from django import forms
from django.utils.translation import gettext_lazy as _

from .base import ChangeSettingsForm


class ChangeThreadsSettingsForm(ChangeSettingsForm):
    settings = [
        "daily_post_limit",
        "hourly_post_limit",
        "post_attachments_limit",
        "post_length_max",
        "post_length_min",
        "thread_title_length_max",
        "thread_title_length_min",
    ]

    daily_post_limit = forms.IntegerField(
        label=_("Daily post limit per user"),
        help_text=_(
            "Daily limit of posts that may be posted by single user. "
            "Fail-safe for situations when forum is flooded by spam bots. "
            "Change to 0 to remove the limit."
        ),
        min_value=0,
    )
    hourly_post_limit = forms.IntegerField(
        label=_("Hourly post limit per user"),
        help_text=_(
            "Hourly limit of posts that may be posted by single user. "
            "Fail-safe for situations when forum is flooded by spam bots. "
            "Change to 0 to remove the limit."
        ),
        min_value=0,
    )
    post_attachments_limit = forms.IntegerField(
        label=_("Maximum number of attachments per post"), min_value=1
    )
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
