from dataclasses import dataclass


@dataclass(frozen=True)
class AttachmentPermissions:
    is_moderator: bool
    can_upload_attachments: bool
    attachment_size_limit: int
    can_delete_own_attachments: bool
