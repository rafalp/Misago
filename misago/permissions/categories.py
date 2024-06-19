from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404

from ..categories.models import Category
from .enums import CategoryPermission
from .proxy import UserPermissionsProxy


def check_category_browse_permission(
    permissions: UserPermissionsProxy,
    category: Category,
    delay_browse_check: bool = False,
):
    if category.id not in permissions.categories[CategoryPermission.SEE]:
        raise Http404()

    if category.id not in permissions.categories[CategoryPermission.BROWSE] and not (
        delay_browse_check and category.delay_browse_check
    ):
        raise PermissionDenied()


def filter_categories_threads_queryset(
    permissions: UserPermissionsProxy, categories: list[int], queryset
):
    if len(categories) == 1:
        category_id = categories[0]
        queryset = queryset.filter(category_id=category_id)
        if category_id not in permissions.categories_moderator:
            queryset = queryset.filter(is_hidden=False)

            if permissions.user.is_authenticated:
                queryset = queryset.filter(
                    Q(is_unapproved=False) | Q(thread_starter=permissions.user)
                )
            else:
                queryset = queryset.filter(is_unapproved=False)

        return queryset

    return queryset
