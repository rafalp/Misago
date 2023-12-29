from django.http import HttpRequest

from ..categories.models import Category
from ..postgres.delete import delete_all
from ..users.models import Group
from .hooks import copy_category_permissions_hook, copy_group_permissions_hook
from .models import CategoryGroupPermission

__all__ = ["copy_category_permissions", "copy_group_permissions"]


def copy_category_permissions(
    src: Category,
    dst: Category,
    request: HttpRequest | None = None,
):
    copy_category_permissions_hook(_copy_category_permissions_action, src, dst, request)


def _copy_category_permissions_action(
    src: Category,
    dst: Category,
    request: HttpRequest | None = None,
) -> None:
    delete_all(CategoryGroupPermission, category_id=dst.id)

    queryset = CategoryGroupPermission.objects.filter(category=src).values_list(
        "group_id", "permission"
    )

    copied_permissions = []
    for group_id, permission in queryset:
        copied_permissions.append(
            CategoryGroupPermission(
                category=dst,
                group_id=group_id,
                permission=permission,
            )
        )

    if copied_permissions:
        CategoryGroupPermission.objects.bulk_create(copied_permissions)


def copy_group_permissions(
    src: Group,
    dst: Group,
    request: HttpRequest | None = None,
) -> None:
    copy_group_permissions_hook(_copy_group_permissions_action, src, dst, request)


def _copy_group_permissions_action(
    src: Group,
    dst: Group,
    request: HttpRequest | None = None,
) -> None:
    _copy_group_category_permissions(src, dst)


def _copy_group_category_permissions(src: Group, dst: Group) -> None:
    delete_all(CategoryGroupPermission, group_id=dst.id)

    queryset = CategoryGroupPermission.objects.filter(group=src).values_list(
        "category_id", "permission"
    )

    copied_permissions = []
    for category_id, permission in queryset:
        copied_permissions.append(
            CategoryGroupPermission(
                group=dst,
                category_id=category_id,
                permission=permission,
            )
        )

    if copied_permissions:
        CategoryGroupPermission.objects.bulk_create(copied_permissions)
