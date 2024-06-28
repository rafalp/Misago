from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.translation import pgettext

from ..categories.models import Category
from .enums import CategoryPermission
from .proxy import UserPermissionsProxy


def check_see_category_permission(
    permissions: UserPermissionsProxy,
    category: Category,
):
    if category.id not in permissions.categories[CategoryPermission.SEE]:
        raise Http404()


def check_browse_category_permission(
    permissions: UserPermissionsProxy,
    category: Category,
    delay_browse_check: bool = False,
):
    check_see_category_permission(permissions, category)

    if category.id not in permissions.categories[CategoryPermission.BROWSE] and not (
        delay_browse_check and category.delay_browse_check
    ):
        raise PermissionDenied(
            pgettext(
                "category permission error",
                "You can't browse the contents of this category.",
            )
        )
