from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext

from ...categories.models import Category
from ..enums import CategoryPermission
from ..proxy import UserPermissionsProxy


def check_can_post_in_closed_category(
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


def check_can_start_thread_in_category(
    permissions: UserPermissionsProxy, category: Category
):
    if category.id not in permissions.categories[CategoryPermission.START]:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't start new threads in this category.",
            )
        )

    check_can_post_in_closed_category(permissions, category)
