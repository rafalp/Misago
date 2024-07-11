from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse

from ..metatags.metatags import get_forum_index_metatags
from .hooks import (
    get_categories_page_component_hook,
    get_categories_page_metatags_hook,
)
from .components import get_categories_data


def index(request, *args, is_index: bool | None = None, **kwargs):
    if not is_index and request.settings.index_view == "categories":
        return redirect(reverse("misago:index"))

    context = {
        "is_index": is_index,
        "categories_list": get_categories_page_component(request),
    }

    context["metatags"] = get_categories_page_metatags(request, context)

    return render(request, "misago/categories/index.html", context)


def get_categories_page_component(request: HttpRequest) -> dict:
    return get_categories_page_component_hook(
        _get_categories_page_component_action, request
    )


def _get_categories_page_component_action(request: HttpRequest) -> dict:
    return {
        "categories": get_categories_data(request),
        "template_name": "misago/categories/component.html",
    }


def get_categories_page_metatags(request: HttpRequest, context: dict) -> dict:
    return get_categories_page_metatags_hook(
        _get_categories_page_metatags_action, request, context
    )


def _get_categories_page_metatags_action(request: HttpRequest, context: dict) -> dict:
    if context["is_index"]:
        return get_forum_index_metatags(request)

    return {}
