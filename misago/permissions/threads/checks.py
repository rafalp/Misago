from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.translation import pgettext

from ...categories.models import Category
from ...threads.models import Thread
from ..categories import check_see_category_permission
from ..enums import CategoryPermission
from ..hooks import (
    check_post_in_closed_category_permission_hook,
    check_see_thread_permission_hook,
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


def check_see_thread_permission(
    permissions: UserPermissionsProxy, category: Category, thread: Thread
):
    check_see_thread_permission_hook(
        _check_see_thread_permission_action, permissions, category, thread
    )


def _check_see_thread_permission_action(
    permissions: UserPermissionsProxy, category: Category, thread: Thread
):
    if not (
        permissions.is_global_moderator
        or category.id in permissions.categories_moderator
    ):
        if thread.is_hidden:
            raise Http404()

        if thread.is_unapproved and (
            thread.starter_id is None
            or permissions.user.is_anonymous
            or thread.starter_id != permissions.user.id
        ):
            raise Http404()

        if (
            category.show_started_only
            and not thread.weight
            and (
                thread.starter_id is None
                or permissions.user.is_anonymous
                or thread.starter_id != permissions.user.id
            )
        ):
            raise Http404()

    check_see_category_permission(permissions, category)

    if category.id not in permissions.categories[CategoryPermission.BROWSE]:
        if category.delay_browse_check:
            raise PermissionDenied(
                pgettext(
                    "category permission error",
                    "You can't browse the contents of this category.",
                )
            )

        raise Http404()
