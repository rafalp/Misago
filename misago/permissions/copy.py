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


COPY_GROUP_PERMISSIONS = (
    "can_edit_own_threads",
    "own_threads_edit_time_limit",
    "can_edit_own_posts",
    "own_posts_edit_time_limit",
    "can_see_others_post_edits",
    "can_hide_own_post_edits",
    "own_post_edits_hide_time_limit",
    "own_delete_post_edits_time_limit",
    "exempt_from_flood_control",
    "can_use_private_threads",
    "can_start_private_threads",
    "private_thread_members_limit",
    "can_upload_attachments",
    "attachment_storage_limit",
    "unused_attachments_storage_limit",
    "attachment_size_limit",
    "can_always_delete_own_attachments",
    "can_start_polls",
    "can_edit_own_polls",
    "own_polls_edit_time_limit",
    "can_close_own_polls",
    "own_polls_close_time_limit",
    "can_vote_in_polls",
    "can_like_posts",
    "can_see_own_post_likes",
    "can_see_others_post_likes",
    "can_change_username",
    "username_changes_limit",
    "username_changes_expire",
    "username_changes_span",
    "can_see_user_profiles",
)


def copy_group_permissions(
    src: Group,
    dst: Group,
    request: HttpRequest | None = None,
) -> None:
    copy_group_permissions_hook(_copy_group_permissions_action, src, dst, request)

    for group_permission in COPY_GROUP_PERMISSIONS:
        setattr(dst, group_permission, getattr(src, group_permission))

    dst.save()


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
