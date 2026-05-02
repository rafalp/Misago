from django import forms
from django.http import HttpRequest
from django.utils.translation import pgettext_lazy

from ..categories.proxy import CategoriesProxy
from ..permissions.enums import CategoryPermission
from ..permissions.proxy import UserPermissionsProxy


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

    for category in categories.categories_list:
        if (
            category["is_vanilla"]
            or category["id"] not in categories_browse
            or category["id"] not in categories_start
        ):
            choices.add(category["id"])

    return choices


class MoveThreadForm(forms.Form):
    request: HttpRequest

    category = forms.TypedChoiceField(
        label=pgettext_lazy("moderation move threads form", "Move to"),
        coerce=int,
        choices=[],
    )

    def __init__(
        self,
        *args,
        request: HttpRequest,
        **kwargs,
    ):
        self.request = request

        super().__init__(*args, **kwargs)

        self.fields["category"].choices = get_category_choices(request.categories)
        self.disabled_choices = get_disabled_category_choices(
            request.user_permissions, request.categories
        )
