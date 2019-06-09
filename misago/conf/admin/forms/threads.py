from django import forms
from django.utils.translation import gettext_lazy as _

from .base import ChangeSettingsForm


class ChangeThreadsSettingsForm(ChangeSettingsForm):
    settings = [
        "attachment_403_image",
        "attachment_404_image",
        "daily_post_limit",
        "hourly_post_limit",
        "post_attachments_limit",
        "post_length_max",
        "post_length_min",
        "readtracker_cutoff",
        "thread_title_length_max",
        "thread_title_length_min",
        "unused_attachments_lifetime",
        "threads_per_page",
        "posts_per_page",
        "posts_per_page_orphans",
        "events_per_page",
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
    unused_attachments_lifetime = forms.IntegerField(
        label=_("Unused attachments lifetime"),
        help_text=_(
            "Period of time (in hours) after which user-uploaded files that weren't "
            "attached to any post are deleted from disk."
        ),
        min_value=1,
    )

    readtracker_cutoff = forms.IntegerField(
        label=_("Read-tracker cutoff"),
        help_text=_(
            "Controls amount of data used by read-tracking system. All content older "
            "than number of days specified in this setting is considered old and read, "
            "even if the opposite is true for the user. Active forums can try lowering "
            "this value while less active ones may wish to increase it instead. "
        ),
        min_value=1,
    )

    threads_per_page = forms.IntegerField(
        label=_("Number of threads displayed on a single page"), min_value=10
    )

    posts_per_page = forms.IntegerField(
        label=_("Number of posts displayed on a single page"), min_value=5
    )
    posts_per_page_orphans = forms.IntegerField(
        label=_("Maximum orphans"),
        help_text=_(
            "If number of posts to be displayed on the last page is less or equal to "
            "number specified in this setting, those posts will instead be displayed "
            "on previous page, reducing the total number of pages in thread."
        ),
        min_value=0,
    )
    events_per_page = forms.IntegerField(
        label=_("Maximum number of events displayed on a single page"), min_value=5
    )

    attachment_403_image = forms.ImageField(
        label=_("Permission denied"),
        help_text=_(
            "Attachments proxy will display this image in place of default one "
            "when user tries to access attachment they have no permission to see."
        ),
        required=False,
    )
    attachment_403_image_delete = forms.BooleanField(
        label=_("Delete custom permission denied image"), required=False
    )
    attachment_404_image = forms.ImageField(
        label=_("Not found"),
        help_text=_(
            "Attachments proxy will display this image in place of default one "
            "when user tries to access attachment that doesn't exist."
        ),
        required=False,
    )
    attachment_404_image_delete = forms.BooleanField(
        label=_("Delete custom not found image"), required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("posts_per_page_orphans") > cleaned_data.get(
            "posts_per_page"
        ):
            self.add_error(
                "posts_per_page_orphans",
                _("This value must be lower than number of posts per page."),
            )
        return cleaned_data
