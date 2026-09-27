from django import forms
from django.utils.translation import pgettext_lazy

from .base import SettingsForm


class SearchSettingsForm(SettingsForm):
    settings = [
        "max_search_query_length",
        "min_search_term_length",
        "user_min_search_interval",
        "guest_min_search_interval",
        "search_log_retention",
    ]

    max_search_query_length = forms.IntegerField(
        label=pgettext_lazy(
            "admin search settings form",
            "Maximum length of a search query",
        ),
        min_value=5,
    )
    min_search_term_length = forms.IntegerField(
        label=pgettext_lazy(
            "admin search settings form",
            "Minimum length of a single term in a search query",
        ),
        help_text=pgettext_lazy(
            "admin search settings form",
            'Search term is either a single word, or a phrase surrounded by quotes.',
        ),
        min_value=1,
    )

    user_min_search_interval = forms.IntegerField(
        label=pgettext_lazy(
            "admin search settings form",
            "User minimum search interval",
        ),
        help_text=pgettext_lazy(
            "admin search settings form",
            "Minimum time in seconds between searches for a single user. Enter 0 to disable.",
        ),
        min_value=0,
    )
    guest_min_search_interval = forms.IntegerField(
        label=pgettext_lazy(
            "admin search settings form",
            "Guest minimum search interval",
        ),
        help_text=pgettext_lazy(
            "admin search settings form",
            "Minimum time in seconds between searches from the same IP address when the user is not signed in. Enter 0 to disable.",
        ),
        min_value=0,
    )

    search_log_retention = forms.IntegerField(
        label=pgettext_lazy(
            "admin search settings form",
            "Retention duration",
        ),
        help_text=pgettext_lazy(
            "admin search settings form",
            "Number of days to keep search logs in the database before they are automatically deleted.",
        ),
        min_value=1,
    )
