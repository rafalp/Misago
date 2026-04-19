from django.http import HttpRequest

from .hooks import context_processor_hook


def plugins(request: HttpRequest) -> dict:
    return context_processor_hook(_context_processor_action, request)


def _context_processor_action(request: HttpRequest) -> dict:
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
