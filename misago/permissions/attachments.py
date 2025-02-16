from dataclasses import dataclass

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.translation import pgettext

from ..attachments.models import Attachment
from ..categories.enums import CategoryTree
from ..categories.models import Category
from ..threads.models import Post, Thread
from .enums import CanUploadAttachments, CategoryPermission
from .hooks import (
    can_upload_private_threads_attachments_hook,
    can_upload_threads_attachments_hook,
    check_delete_attachment_permission_hook,
    check_download_attachment_permission_hook,
)
from .privatethreads import (
    check_private_threads_permission,
    check_see_private_thread_permission,
    check_see_private_thread_post_permission,
)
from .proxy import UserPermissionsProxy
from .threads import check_see_thread_post_permission, check_see_thread_permission

__all__ = [
    "AttachmentsPermissions",
    "can_upload_private_threads_attachments",
    "can_upload_threads_attachments",
    "get_threads_attachments_permissions",
    "get_private_threads_attachments_permissions",
]


def can_upload_threads_attachments(
    permissions: UserPermissionsProxy, category: Category
) -> bool:
    return can_upload_threads_attachments_hook(
        _can_upload_threads_attachments_action, permissions, category
    )


def _can_upload_threads_attachments_action(
    permissions: UserPermissionsProxy, category: Category
) -> bool:
    return (
        permissions.can_upload_attachments != CanUploadAttachments.NEVER
        and category.id in permissions.categories[CategoryPermission.ATTACHMENTS]
    )


def can_upload_private_threads_attachments(permissions: UserPermissionsProxy) -> bool:
    return can_upload_private_threads_attachments_hook(
        _can_upload_private_threads_attachments_action, permissions
    )


def _can_upload_private_threads_attachments_action(
    permissions: UserPermissionsProxy,
) -> bool:
    return permissions.can_upload_attachments == CanUploadAttachments.EVERYWHERE


def check_download_attachment_permission(
    permissions: UserPermissionsProxy,
    category: Category | None,
    thread: Thread | None,
    post: Post | None,
    attachment: Attachment,
):
    return check_download_attachment_permission_hook(
        _check_download_attachment_permission_action,
        permissions,
        category,
        thread,
        post,
        attachment,
    )


def _check_download_attachment_permission_action(
    permissions: UserPermissionsProxy,
    category: Category | None,
    thread: Thread | None,
    post: Post | None,
    attachment: Attachment,
):
    if permissions.user.is_authenticated and (
        permissions.user.id == attachment.uploader_id
        or permissions.user.is_misago_admin
    ):
        return  # Uploaders and admins can always download attachments

    if not (category and thread and post):
        raise Http404()  # Skip remaining permission checks

    if category.tree_id == CategoryTree.THREADS:
        try:
            check_see_thread_permission(permissions, category, thread)
            check_see_thread_post_permission(permissions, category, thread, post)
        except PermissionDenied as exc:
            raise Http404() from exc

        if category.id not in permissions.categories[CategoryPermission.ATTACHMENTS]:
            raise PermissionDenied(
                pgettext(
                    "attachment permission error",
                    "You can't download attachments in this category.",
                )
            )

    elif category.tree_id == CategoryTree.PRIVATE_THREADS:
        try:
            check_private_threads_permission(permissions)
            check_see_private_thread_permission(permissions, thread)
            check_see_private_thread_post_permission(permissions, thread, post)
        except PermissionDenied as exc:
            raise Http404() from exc

    else:
        raise Http404()


def check_delete_attachment_permission(
    permissions: UserPermissionsProxy,
    category: Category | None,
    thread: Thread | None,
    post: Post | None,
    attachment: Attachment,
):
    return check_delete_attachment_permission_hook(
        _check_delete_attachment_permission_action,
        permissions,
        category,
        thread,
        post,
        attachment,
    )


def _check_delete_attachment_permission_action(
    permissions: UserPermissionsProxy,
    category: Category | None,
    thread: Thread | None,
    post: Post | None,
    attachment: Attachment,
):
    if not permissions.user.is_authenticated:
        raise PermissionDenied(
            pgettext("attachment permission error", "You can't delete attachments.")
        )

    if permissions.user.is_misago_admin or permissions.is_global_moderator:
        return  # Admins can always delete attachments

    if (
        not (category and thread and post)
        and permissions.user.id == attachment.uploader_id
    ):
        return  # Uploaders can always delete their own unused attachments

    if category and category.tree_id in (
        CategoryTree.THREADS,
        CategoryTree.PRIVATE_THREADS,
    ):
        if (
            category.tree_id == CategoryTree.THREADS
            and permissions.is_category_moderator(category.id)
        ) or (
            category.tree_id == CategoryTree.PRIVATE_THREADS
            and permissions.is_private_threads_moderator
        ):
            return

        if permissions.user.id != attachment.uploader_id:
            raise PermissionDenied(
                pgettext(
                    "attachment permission error",
                    "You can't delete other users attachments.",
                )
            )

        if not permissions.can_always_delete_own_attachments:
            raise PermissionDenied(
                pgettext(
                    "attachment permission error",
                    "You can't delete your own attachments once they're associated with a post.",
                )
            )

    else:
        raise PermissionDenied(
            pgettext("attachment permission error", "You can't delete attachments.")
        )
