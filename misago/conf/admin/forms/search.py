from django import forms
from django.utils.translation import pgettext_lazy

from .base import SettingsForm


class SearchSettingsForm(SettingsForm):
    settings = [
        "search_threads_query_max_length",
        "search_threads_term_min_length",
        "search_threads_min_interval_user",
        "search_threads_min_interval_guest",
        "search_threads_batch_size",
        "search_threads_max_offset",
        "search_threads_log_retention",
        "search_users_max_results",
        "search_users_max_candidates",
        "search_users_max_suggestions",
    ]

    search_threads_query_max_length = forms.IntegerField(
        label=pgettext_lazy(
            "admin search settings form",
            "Maximum length of a search query",
        ),
        min_value=5,
    )
    search_threads_term_min_length = forms.IntegerField(
        label=pgettext_lazy(
            "admin search settings form",
            "Minimum length of a single term in a search query",
        ),
        help_text=pgettext_lazy(
            "admin search settings form",
            "Search term is either a single word, or a phrase surrounded by quotes.",
        ),
        min_value=1,
    )

    search_threads_min_interval_user = forms.IntegerField(
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
    search_threads_min_interval_guest = forms.IntegerField(
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

    search_threads_batch_size = forms.IntegerField(
        label=pgettext_lazy(
            "admin search settings form",
            "Results per batch",
        ),
        help_text=pgettext_lazy(
            "admin search settings form",
            "Number of search results returned in a single batch.",
        ),
        min_value=1,
    )
    search_threads_max_offset = forms.IntegerField(
        label=pgettext_lazy(
            "admin search settings form",
            "Maximum offset",
        ),
        help_text=pgettext_lazy(
            "admin search settings form",
            "Maximum search results offset allowed when loading additional batches. Should be divisible by the batch size.",
        ),
        min_value=1,
    )

    search_threads_log_retention = forms.IntegerField(
        label=pgettext_lazy(
            "admin search settings form",
            "Log retention duration",
        ),
        help_text=pgettext_lazy(
            "admin search settings form",
            "Number of days to keep search logs in the database before they are automatically deleted.",
        ),
        min_value=1,
    )

    search_users_max_results = forms.IntegerField(
        label=pgettext_lazy(
            "admin search settings form",
            "Maximum search results",
        ),
        help_text=pgettext_lazy(
            "admin search settings form",
            "Maximum number of search results to display.",
        ),
        min_value=1,
    )
    search_users_max_candidates = forms.IntegerField(
        label=pgettext_lazy(
            "admin search settings form",
            "Maximum candidates",
        ),
        help_text=pgettext_lazy(
            "admin search settings form",
            "Maximum number of matching users to retrieve from the database before applying the second ranking.",
        ),
        min_value=1,
    )
    search_users_max_suggestions = forms.IntegerField(
        label=pgettext_lazy(
            "admin search settings form",
            "Maximum suggestions",
        ),
        help_text=pgettext_lazy(
            "admin search settings form",
            "Maximum number of user suggestions to display for mentions and user select form fields.",
        ),
        min_value=1,
    )
