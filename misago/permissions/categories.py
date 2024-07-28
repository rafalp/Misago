from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.translation import pgettext

from ..categories.models import Category
from .enums import CategoryPermission
from .hooks import (
    check_browse_category_permission_hook,
    check_see_category_permission_hook,
)
from .proxy import UserPermissionsProxy


def check_see_category_permission(
    permissions: UserPermissionsProxy,
    category: Category,
):
    check_see_category_permission_hook(
        _check_see_category_permission_action, permissions, category
    )


def _check_see_category_permission_action(
    permissions: UserPermissionsProxy,
    category: Category,
):
    if category.id not in permissions.categories[CategoryPermission.SEE]:
        raise Http404()


def check_browse_category_permission(
    permissions: UserPermissionsProxy,
    category: Category,
    can_delay: bool = False,
):
    check_browse_category_permission_hook(
        _check_browse_category_permission_action,
        permissions,
        category,
        can_delay,
    )


def _check_browse_category_permission_action(
    permissions: UserPermissionsProxy,
    category: Category,
    can_delay: bool = False,
):
    check_see_category_permission(permissions, category)

    if category.id not in permissions.categories[CategoryPermission.BROWSE] and not (
        can_delay and category.delay_browse_check
    ):
        raise PermissionDenied(
            pgettext(
                "category permission error",
                "You can't browse the contents of this category.",
            )
        )
