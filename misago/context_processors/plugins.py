from django.http import HttpRequest

from .hooks import get_context_data_hook


def plugins(request: HttpRequest) -> dict:
    return get_context_data_hook(_get_context_data_action, request)


def _get_context_data_action(request: HttpRequest) -> dict:
    context_data = {
        "before_head_close": [],
        "after_body_open": [],
        "before_body_close": [],
        "above_navbar": [],
        "below_navbar": [],
        "above_footer": [],
        "below_footer": [],
    }

    return context_data
