from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import pgettext

from ..categories.models import Category
from .hooks import (
    get_category_breadcrumbs_hook,
    get_thread_breadcrumbs_hook,
    get_threads_breadcrumbs_hook,
)
from .models import Thread


def get_threads_breadcrumbs(request: HttpRequest) -> dict:
    return get_threads_breadcrumbs_hook(_get_threads_breadcrumbs_action, request)


def _get_threads_breadcrumbs_action(request: HttpRequest) -> dict:
    if request.settings.index_view == "threads":
        breadcrumb = {
            "type": "index",
            "label": pgettext("breadcrumb", "Home"),
            "url": reverse("misago:index"),
        }
    else:
        breadcrumb = {
            "type": "threads",
            "label": pgettext("breadcrumb", "Threads"),
            "url": reverse("misago:thread-list"),
        }

    return {
        "id": "breadcrumbs",
        "template_name": "misago/threads_breadcrumbs.html",
        "items": [breadcrumb],
    }


def get_category_breadcrumbs(
    request: HttpRequest, category: Category, include_category: bool = False
) -> dict:
    return get_category_breadcrumbs_hook(
        _get_category_breadcrumbs_action, request, category, include_category
    )


def _get_category_breadcrumbs_action(
    request: HttpRequest, category: Category, include_category: bool = False
) -> dict:
    items = [
        {
            "type": "index",
            "label": pgettext("breadcrumb", "Home"),
            "url": reverse("misago:index"),
        }
    ]

    for item in request.categories.get_category_path(category.id, include_category):
        items.append(
            {
                "type": "category",
                "label": item["name"],
                "short_label": item["short_name"],
                "color": item["color"],
                "css_class": item["css_class"],
                "url": item["url"],
            }
        )

    return {
        "id": "breadcrumbs",
        "template_name": "misago/category_breadcrumbs.html",
        "items": items,
    }


def get_thread_breadcrumbs(request: HttpRequest, thread: Thread) -> dict:
    return get_thread_breadcrumbs_hook(_get_thread_breadcrumbs_action, request, thread)


def _get_thread_breadcrumbs_action(request: HttpRequest, thread: Thread) -> dict:
    items = [
        {
            "type": "index",
            "label": pgettext("breadcrumb", "Home"),
            "url": reverse("misago:index"),
        }
    ]

    for item in request.categories.get_category_path(thread.category_id, True):
        items.append(
            {
                "type": "category",
                "label": item["name"],
                "short_label": item["short_name"],
                "color": item["color"],
                "css_class": item["css_class"],
                "url": item["url"],
            }
        )

    items.append(
        {
            "type": "thread",
            "label": thread.title,
            "url": reverse(
                "misago:thread",
                kwargs={"thread_id": thread.id, "slug": thread.slug},
            ),
        }
    )

    return {
        "id": "breadcrumbs",
        "template_name": "misago/thread_breadcrumbs.html",
        "items": items,
    }
