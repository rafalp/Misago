from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext

from ...categories.models import Category
from ..enums import CategoryPermission
from ..hooks import (
    check_post_in_closed_category_permission_hook,
    check_start_thread_in_category_permission_hook,
)
from ..proxy import UserPermissionsProxy


def check_post_in_closed_category_permission(
    permissions: UserPermissionsProxy, category: Category
):
    check_post_in_closed_category_permission_hook(
        _check_post_in_closed_category_permission_action,
        permissions,
        category,
    )


def _check_post_in_closed_category_permission_action(
    permissions: UserPermissionsProxy, category: Category
):
    if category.is_closed and not (
        permissions.is_global_moderator
        or category.id in permissions.categories_moderator
    ):
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "This category is closed.",
            )
        )


def check_start_thread_in_category_permission(
    permissions: UserPermissionsProxy, category: Category
):
    check_start_thread_in_category_permission_hook(
        _check_start_thread_in_category_permission_action,
        permissions,
        category,
    )


def _check_start_thread_in_category_permission_action(
    permissions: UserPermissionsProxy, category: Category
):
    if category.id not in permissions.categories[CategoryPermission.START]:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't start new threads in this category.",
            )
        )

    check_post_in_closed_category_permission(permissions, category)
