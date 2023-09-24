from django import forms
from django.utils.translation import pgettext_lazy

from .base import SettingsForm


class ThreadsSettingsForm(SettingsForm):
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
        label=pgettext_lazy("admin threads settings form", "Daily post limit per user"),
        help_text=pgettext_lazy(
            "admin threads settings form",
            "Daily limit of posts that may be posted by single user. Fail-safe for situations when forum is flooded by spam bots. Change to 0 to remove the limit.",
        ),
        min_value=0,
    )
    hourly_post_limit = forms.IntegerField(
        label=pgettext_lazy(
            "admin threads settings form", "Hourly post limit per user"
        ),
        help_text=pgettext_lazy(
            "admin threads settings form",
            "Hourly limit of posts that may be posted by single user. Fail-safe for situations when forum is flooded by spam bots. Change to 0 to remove the limit.",
        ),
        min_value=0,
    )
    post_attachments_limit = forms.IntegerField(
        label=pgettext_lazy(
            "admin threads settings form", "Maximum number of attachments per post"
        ),
        min_value=1,
    )
    post_length_max = forms.IntegerField(
        label=pgettext_lazy(
            "admin threads settings form", "Maximum allowed post length"
        ),
        min_value=0,
    )
    post_length_min = forms.IntegerField(
        label=pgettext_lazy(
            "admin threads settings form", "Minimum required post length"
        ),
        min_value=1,
    )
    thread_title_length_max = forms.IntegerField(
        label=pgettext_lazy(
            "admin threads settings form", "Maximum allowed thread title length"
        ),
        min_value=2,
        max_value=255,
    )
    thread_title_length_min = forms.IntegerField(
        label=pgettext_lazy(
            "admin threads settings form", "Minimum required thread title length"
        ),
        min_value=2,
        max_value=255,
    )
    unused_attachments_lifetime = forms.IntegerField(
        label=pgettext_lazy(
            "admin threads settings form", "Unused attachments lifetime"
        ),
        help_text=pgettext_lazy(
            "admin threads settings form",
            "Period of time (in hours) after which user-uploaded files that weren't attached to any post are deleted from disk.",
        ),
        min_value=1,
    )

    readtracker_cutoff = forms.IntegerField(
        label=pgettext_lazy("admin threads settings form", "Read-tracker cutoff"),
        help_text=pgettext_lazy(
            "admin threads settings form",
            "Controls amount of data used by read-tracking system. All content older than number of days specified in this setting is considered old and read, even if the opposite is true for the user. Active forums can try lowering this value while less active ones may wish to increase it instead.",
        ),
        min_value=1,
    )

    threads_per_page = forms.IntegerField(
        label=pgettext_lazy(
            "admin threads settings form",
            "Number of threads displayed on a single page",
        ),
        min_value=10,
    )

    posts_per_page = forms.IntegerField(
        label=pgettext_lazy(
            "admin threads settings form", "Number of posts displayed on a single page"
        ),
        min_value=5,
    )
    posts_per_page_orphans = forms.IntegerField(
        label=pgettext_lazy("admin threads settings form", "Maximum orphans"),
        help_text=pgettext_lazy(
            "admin threads settings form",
            "This setting prevents situations when the last page of a thread contains very few items. If number of posts to be displayed on the last page is less or equal to number specified in this setting, those posts will instead be appended to the previous page, reducing number of thread's pages.",
        ),
        min_value=0,
    )
    events_per_page = forms.IntegerField(
        label=pgettext_lazy(
            "admin threads settings form",
            "Maximum number of events displayed on a single page",
        ),
        min_value=5,
    )

    attachment_403_image = forms.ImageField(
        label=pgettext_lazy("admin threads settings form", "Permission denied"),
        help_text=pgettext_lazy(
            "admin threads settings form",
            "Attachments proxy will display this image in place of default one when user tries to access attachment they have no permission to see.",
        ),
        required=False,
    )
    attachment_403_image_delete = forms.BooleanField(
        label=pgettext_lazy(
            "admin threads settings form", "Delete custom permission denied image"
        ),
        required=False,
    )
    attachment_404_image = forms.ImageField(
        label=pgettext_lazy("admin threads settings form", "Not found"),
        help_text=pgettext_lazy(
            "admin threads settings form",
            "Attachments proxy will display this image in place of default one when user tries to access attachment that doesn't exist.",
        ),
        required=False,
    )
    attachment_404_image_delete = forms.BooleanField(
        label=pgettext_lazy(
            "admin threads settings form", "Delete custom not found image"
        ),
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("posts_per_page_orphans") > cleaned_data.get(
            "posts_per_page"
        ):
            self.add_error(
                "posts_per_page_orphans",
                pgettext_lazy(
                    "admin threads settings form",
                    "This value must be lower than number of posts per page.",
                ),
            )
        return cleaned_data
