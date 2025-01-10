from django import forms
from django.utils.translation import pgettext_lazy

from ....admin.forms import YesNoSwitch
from ....attachments.enums import AllowedAttachments
from ....categories.enums import CategoryChildrenComponent
from ....threads.enums import ThreadsListsPolling
from .base import SettingsForm


class ThreadsSettingsForm(SettingsForm):
    settings = [
        "allowed_attachment_types",
        "allow_private_threads_attachments",
        "attachment_403_image",
        "attachment_404_image",
        "attachment_image_max_width",
        "attachment_image_max_height",
        "attachment_thumbnail_width",
        "attachment_thumbnail_height",
        "flood_control",
        "merge_concurrent_posts",
        "post_attachments_limit",
        "post_length_max",
        "post_length_min",
        "readtracker_cutoff",
        "thread_title_length_max",
        "thread_title_length_min",
        "unused_attachments_lifetime",
        "threads_per_page",
        "threads_list_item_categories_component",
        "threads_list_categories_component",
        "threads_lists_polling",
        "posts_per_page",
        "posts_per_page_orphans",
        "events_per_page",
    ]

    flood_control = forms.IntegerField(
        label=pgettext_lazy(
            "admin threads settings form",
            "Flood control",
        ),
        help_text=pgettext_lazy(
            "admin threads settings form",
            "Number of seconds that must pass after a user posts before they can post again. Edits and concurrent posts are excluded from this limit. Enter zero to disable this feature.",
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
            "Time (in hours) after which user-uploaded files that weren't attached to any post are deleted from disk.",
        ),
        min_value=1,
    )

    merge_concurrent_posts = forms.IntegerField(
        label=pgettext_lazy(
            "admin threads settings form",
            "Automatically merge concurrent posts made within specified time",
        ),
        help_text=pgettext_lazy(
            "admin threads settings form",
            "Time (in minutes) during which user's newly posted reply to a thread will be appended to their last post. The last post must be editable by the user. Enter zero to disable this feature.",
        ),
        min_value=0,
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
    threads_list_item_categories_component = forms.CharField(
        label=pgettext_lazy(
            "admin threads settings form", "Thread's categories appearance"
        ),
        help_text=pgettext_lazy(
            "admin threads settings form",
            "Select UI for displaying threads categories on threads lists.",
        ),
        widget=forms.RadioSelect(
            choices=(
                (
                    "breadcrumbs",
                    pgettext_lazy(
                        "admin threads item categories choice", "Breadcrumbs"
                    ),
                ),
                (
                    "labels",
                    pgettext_lazy("admin threads item categories choice", "Labels"),
                ),
            )
        ),
    )
    threads_lists_polling = forms.IntegerField(
        label=pgettext_lazy(
            "admin threads settings form",
            "Enable polling for new or updated threads",
        ),
        help_text=pgettext_lazy(
            "admin threads settings form",
            "Enabling polling will make threads lists call the server every minute for the number of new or updated threads. If there are new threads, a button will be displayed for the user that will let them refresh the list without having to refresh the entire page.",
        ),
        widget=forms.RadioSelect(
            choices=ThreadsListsPolling.get_choices(),
        ),
    )

    threads_list_categories_component = forms.CharField(
        label=pgettext_lazy("admin threads settings form", "Categories UI component"),
        help_text=pgettext_lazy(
            "admin threads settings form",
            "Select UI component to use for displaying list of categories on the threads page.",
        ),
        widget=forms.RadioSelect(
            choices=CategoryChildrenComponent.get_threads_choices(),
        ),
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

    allowed_attachment_types = forms.CharField(
        label=pgettext_lazy("admin threads settings form", "Allowed attachment types"),
        help_text=pgettext_lazy(
            "admin threads settings form",
            'This setting controls which files can be uploaded as attachments. Select the "Disable" option to disable new attachment uploads.',
        ),
        widget=forms.RadioSelect(
            choices=AllowedAttachments.get_choices(),
        ),
    )
    allow_private_threads_attachments = YesNoSwitch(
        label=pgettext_lazy(
            "admin oauth2 settings form",
            "Allow uploading attachments in private threads",
        ),
    )

    attachment_image_max_width = forms.IntegerField(
        label=pgettext_lazy("admin threads settings form", "Maximum image dimensions"),
        help_text=pgettext_lazy(
            "admin threads settings form",
            "This setting controls the maximum dimensions of uploaded images, in pixels. Images exceeding these dimensions will be scaled down.",
        ),
        min_value=100,
    )
    attachment_image_max_height = forms.IntegerField(min_value=100)

    attachment_thumbnail_width = forms.IntegerField(
        label=pgettext_lazy(
            "admin threads settings form", "Image thumbnail dimensions"
        ),
        help_text=pgettext_lazy(
            "admin threads settings form",
            "Dimensions, in pixels, of the thumbnail image to be generated if the uploaded image exceeds the specified size.",
        ),
        min_value=100,
    )
    attachment_thumbnail_height = forms.IntegerField(min_value=100)

    attachment_403_image = forms.ImageField(
        label=pgettext_lazy("admin threads settings form", "Permission denied image"),
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
        label=pgettext_lazy("admin threads settings form", "Not found image"),
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

        posts_per_page_orphans = cleaned_data.get("posts_per_page_orphans")
        posts_per_page = cleaned_data.get("posts_per_page")

        if (
            posts_per_page_orphans is not None
            and posts_per_page is not None
            and posts_per_page_orphans >= posts_per_page
        ):
            self.add_error(
                "posts_per_page_orphans",
                pgettext_lazy(
                    "admin threads settings form",
                    "This value must be lower than number of posts per page.",
                ),
            )

        attachment_image_max_width = cleaned_data.get("attachment_image_max_width")
        attachment_thumbnail_width = cleaned_data.get("attachment_thumbnail_width")

        if (
            attachment_image_max_width is not None
            and attachment_thumbnail_width is not None
            and attachment_thumbnail_width >= attachment_image_max_width
        ):
            self.add_error(
                "attachment_thumbnail_width",
                pgettext_lazy(
                    "admin threads settings form",
                    "This value must be lower than the image width limit.",
                ),
            )

        attachment_image_max_height = cleaned_data.get("attachment_image_max_height")
        attachment_thumbnail_height = cleaned_data.get("attachment_thumbnail_height")

        if (
            attachment_image_max_height is not None
            and attachment_thumbnail_height is not None
            and attachment_thumbnail_height >= attachment_image_max_height
        ):
            self.add_error(
                "attachment_thumbnail_height",
                pgettext_lazy(
                    "admin threads settings form",
                    "This value must be lower than the image height limit.",
                ),
            )

        return cleaned_data
