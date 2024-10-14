from django import forms
from django.http import HttpRequest
from django.utils.translation import pgettext_lazy

from ..categories.proxy import CategoriesProxy
from ..permissions.enums import CategoryPermission
from ..permissions.proxy import UserPermissionsProxy
from ..threads.models import Thread


def get_category_choices(
    categories: CategoriesProxy, *, allow_empty: bool = True
) -> list[tuple[int, str]]:
    choices: list[tuple[int, str]] = []
    if allow_empty:
        choices.append(
            ("", pgettext_lazy("moderation form empty_category", "Select category"))
        )

    for category in categories.categories_list:
        prefix = " → " * category["level"]
        choices.append((category["id"], prefix + category["name"]))
    return choices


def get_disabled_category_choices(
    user_permissions: UserPermissionsProxy,
    categories: CategoriesProxy,
) -> set[int]:
    choices: set[int] = set()

    categories_browse = user_permissions.categories[CategoryPermission.BROWSE]
    categories_start = user_permissions.categories[CategoryPermission.START]
    moderated_categories = user_permissions.moderated_categories

    for category in categories.categories_list:
        if (
            category["is_vanilla"]
            or category["id"] not in categories_browse
            or category["id"] not in categories_start
            or (category["is_closed"] and category["id"] not in moderated_categories)
        ):
            choices.add(category["id"])

    return choices


class MoveThreads(forms.Form):
    threads: list[Thread]
    request: HttpRequest

    category = forms.TypedChoiceField(
        label=pgettext_lazy("moderation move threads form", "Move to category"),
        coerce=int,
        choices=[],
    )

    def __init__(
        self,
        data: dict | None = None,
        *,
        threads: list[Thread],
        request: HttpRequest,
    ):
        super().__init__(data, prefix="moderation")

        self.fields["category"].choices = get_category_choices(request.categories)
        self.disabled_choices = get_disabled_category_choices(
            request.user_permissions, request.categories
        )

        self.threads = threads
        self.request = request
