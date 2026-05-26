from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import pgettext

from ..categories.models import Category
from .hooks import get_category_breadcrumbs_hook, get_thread_breadcrumbs_hook
from .models import Thread


def get_category_breadcrumbs(
    request: HttpRequest, category: Category, include_category: bool = False
) -> list[dict]:
    return get_category_breadcrumbs_hook(
        _get_category_breadcrumbs_action, request, category, include_category
    )


def _get_category_breadcrumbs_action(
    request: HttpRequest, category: Category, include_category: bool = False
) -> list[dict]:
    items = [
        {
            "type": "index",
            "label": pgettext("index breadcrumb", "Home"),
            "url": reverse("misago:index"),
        }
    ]

    for category in request.categories.get_category_path(category.id, include_category):
        items.append(
            {
                "type": "category",
                "label": category["name"],
                "short_label": category["short_name"],
                "color": category["color"],
                "css_class": category["css_class"],
                "url": category["url"],
            }
        )

    return {
        "id": "breadcrumbs",
        "template_name": "misago/category_breadcrumbs.html",
        "items": items,
    }


def get_thread_breadcrumbs(request: HttpRequest, thread: Thread) -> list[dict]:
    return get_thread_breadcrumbs_hook(_get_thread_breadcrumbs_action, request, thread)


def _get_thread_breadcrumbs_action(request: HttpRequest, thread: Thread) -> list[dict]:
    items = [
        {
            "type": "index",
            "label": pgettext("index breadcrumb", "Home"),
            "url": reverse("misago:index"),
        }
    ]

    for category in request.categories.get_category_path(category.id, True):
        items.append(
            {
                "type": "category",
                "label": category["name"],
                "short_label": category["short_name"],
                "color": category["color"],
                "css_class": category["css_class"],
                "url": category["url"],
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
