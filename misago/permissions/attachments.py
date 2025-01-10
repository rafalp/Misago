from dataclasses import dataclass

from .enums import CanUploadAttachments, CategoryPermission
from .proxy import UserPermissionsProxy


@dataclass(frozen=True)
class AttachmentPermissions:
    is_moderator: bool
    can_upload_attachments: bool
    attachment_size_limit: int
    can_delete_own_attachments: bool


def get_threads_attachments_permissions(
    user_permissions: UserPermissionsProxy, category_id: int
) -> AttachmentPermissions:
    category_permission = (
        category_id in user_permissions.categories[CategoryPermission.ATTACHMENTS]
    )

    if not category_permission or user_permissions.user.is_anonymous:
        return AttachmentPermissions(
            is_moderator=False,
            can_upload_attachments=False,
            attachment_size_limit=0,
            can_delete_own_attachments=False,
        )

    return AttachmentPermissions(
        is_moderator=user_permissions.is_category_moderator(category_id),
        can_upload_attachments=bool(user_permissions.can_upload_attachments),
        attachment_size_limit=user_permissions.attachment_size_limit,
        can_delete_own_attachments=user_permissions.can_delete_own_attachments,
    )


def get_private_threads_attachments_permissions(
    user_permissions: UserPermissionsProxy,
) -> AttachmentPermissions:
    if user_permissions.user.is_anonymous:
        return AttachmentPermissions(
            is_moderator=False,
            can_upload_attachments=False,
            attachment_size_limit=0,
            can_delete_own_attachments=False,
        )

    return AttachmentPermissions(
        is_moderator=user_permissions.is_private_threads_moderator,
        can_upload_attachments=(
            user_permissions.can_upload_attachments == CanUploadAttachments.EVERYWHERE
        ),
        attachment_size_limit=user_permissions.attachment_size_limit,
        can_delete_own_attachments=user_permissions.can_delete_own_attachments,
    )
