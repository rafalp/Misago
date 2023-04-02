from django import forms
from django.utils.translation import pgettext_lazy

from ....notifications.threads import ThreadNotifications
from .base import SettingsForm


class NotificationsSettingsForm(SettingsForm):
    settings = [
        "watch_started_threads",
        "watch_replied_threads",
        "watch_new_private_threads_by_followed",
        "watch_new_private_threads_by_other_users",
        "notify_new_private_threads_by_followed",
        "notify_new_private_threads_by_other_users",
        "delete_notifications_older_than",
    ]

    watch_started_threads = forms.TypedChoiceField(
        label=pgettext_lazy(
            "admin notifications",
            "Notify about new replies in threads started by the user",
        ),
        choices=ThreadNotifications.choices,
        widget=forms.RadioSelect(),
        coerce=int,
    )
    watch_replied_threads = forms.TypedChoiceField(
        label=pgettext_lazy(
            "admin notifications",
            "Notify about new replies in threads replied by the user",
        ),
        choices=ThreadNotifications.choices,
        widget=forms.RadioSelect(),
        coerce=int,
    )

    watch_new_private_threads_by_followed = forms.TypedChoiceField(
        label=pgettext_lazy(
            "admin notifications",
            "Notify about new replies in new private threads started by followed users",
        ),
        choices=ThreadNotifications.choices,
        widget=forms.RadioSelect(),
        coerce=int,
    )
    watch_new_private_threads_by_other_users = forms.TypedChoiceField(
        label=pgettext_lazy(
            "admin notifications",
            "Notify about new replies in new private threads started by other users",
        ),
        choices=ThreadNotifications.choices,
        widget=forms.RadioSelect(),
        coerce=int,
    )

    notify_new_private_threads_by_followed = forms.TypedChoiceField(
        label=pgettext_lazy(
            "admin notifications",
            "Notify about new private threads started by followed users",
        ),
        choices=ThreadNotifications.choices,
        widget=forms.RadioSelect(),
        coerce=int,
    )
    notify_new_private_threads_by_other_users = forms.TypedChoiceField(
        label=pgettext_lazy(
            "admin notifications",
            "Notify about new private threads started by other users",
        ),
        choices=ThreadNotifications.choices,
        widget=forms.RadioSelect(),
        coerce=int,
    )

    delete_notifications_older_than = forms.IntegerField(
        label=pgettext_lazy(
            "admin notifications",
            "Automatically delete notifications that are older than given number of days",
        ),
        help_text=pgettext_lazy(
            "admin notifications",
            "Old notifications filling the database table can have an negative impact on the notifications performance.",
        ),
        min_value=1,
    )
