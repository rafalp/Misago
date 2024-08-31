from typing import TYPE_CHECKING

from django.contrib import messages
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import pgettext

from ..metatags.metatags import get_forum_index_metatags
from ..readtracker.models import ReadCategory, ReadThread
from .hooks import (
    get_categories_page_component_hook,
    get_categories_page_metatags_hook,
)
from .components import get_categories_data

if TYPE_CHECKING:
    from ..users.models import User


def index(request, *args, is_index: bool | None = None, **kwargs):
    if not is_index and request.settings.index_view == "categories":
        return redirect(reverse("misago:index"))

    if (
        request.method == "POST"
        and "mark_as_read" in request.POST
        and request.user.is_authenticated
    ):
        if response := mark_as_read(request):
            return response

    context = {
        "is_index": is_index,
        "categories_list": get_categories_page_component(request),
    }

    context["metatags"] = get_categories_page_metatags(request, context)

    if request.is_htmx:
        template_name = "misago/categories/partial.html"
    else:
        template_name = "misago/categories/index.html"

    return render(request, template_name, context)


def mark_as_read(request: HttpRequest) -> HttpResponse | None:
    if not request.POST.get("confirm"):
        return render(request, "misago/categories/mark_as_read_page.html")

    if categories_ids := list(request.categories.categories):
        read_all_categories(request.user, categories_ids)
        messages.success(
            request, pgettext("mark categories as read", "Categories marked as read")
        )

    if request.is_htmx:
        return None

    if request.settings.index_view == "categories":
        return redirect(reverse("misago:index"))

    return redirect(reverse("misago:categories"))


@transaction.atomic
def read_all_categories(user: "User", categories_ids: list[int]):
    read_time = timezone.now()

    # Clear read tracker for categories
    ReadThread.objects.filter(user=user, category_id__in=categories_ids).delete()
    ReadCategory.objects.filter(user=user, category_id__in=categories_ids).delete()

    ReadCategory.objects.bulk_create(
        ReadCategory(user=user, read_time=read_time, category_id=category_id)
        for category_id in categories_ids
    )


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
