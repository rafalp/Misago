from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import pgettext

from ..categories.models import Category
from ..threads.models import Thread
from .hooks import (
    get_private_thread_breadcrumbs_hook,
    get_private_threads_breadcrumbs_hook,
)


def get_private_threads_breadcrumbs(request: HttpRequest) -> dict:
    return get_private_threads_breadcrumbs_hook(
        _get_private_threads_breadcrumbs_action, request
    )


def _get_private_threads_breadcrumbs_action(request: HttpRequest) -> dict:
    return {
        "id": "breadcrumbs",
        "template_name": "misago/private_threads_breadcrumbs.html",
        "items": [
            {
                "type": "private_threads",
                "label": pgettext("breadcrumb", "Private threads"),
                "url": reverse("misago:private-thread-list"),
            },
        ],
    }


def get_private_thread_breadcrumbs(request: HttpRequest, thread: Thread) -> dict:
    return get_private_thread_breadcrumbs_hook(
        _get_private_thread_breadcrumbs_action, request, thread
    )


def _get_private_thread_breadcrumbs_action(
    request: HttpRequest, thread: Thread
) -> dict:
    return {
        "id": "breadcrumbs",
        "template_name": "misago/private_thread_breadcrumbs.html",
        "items": [
            {
                "type": "private_threads",
                "label": pgettext("breadcrumb", "Private threads"),
                "url": reverse("misago:private-thread-list"),
            },
            {
                "type": "private_thread",
                "label": thread.title,
                "url": reverse(
                    "misago:private-thread",
                    kwargs={"thread_id": thread.id, "slug": thread.slug},
                ),
            },
        ],
    }
