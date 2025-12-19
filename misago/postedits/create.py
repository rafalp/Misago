from datetime import datetime
from typing import TYPE_CHECKING, Union

from django.http import HttpRequest

from ..attachments.models import Attachment
from ..threads.models import Post
from ..core.utils import slugify
from .diff import diff_text
from .hooks import create_post_edit_hook
from .models import PostEdit

if TYPE_CHECKING:
    from ..users.models import User


def create_post_edit(
    *,
    post: Post,
    user: Union["User", str],
    edit_reason: str | None,
    old_content: str,
    attachments: list[Attachment] | None = None,
    deleted_attachments: list[Attachment] | None = None,
    edited_at: datetime | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> PostEdit:
    return create_post_edit_hook(
        _create_post_edit_action,
        post=post,
        user=user,
        edit_reason=edit_reason,
        old_content=old_content,
        attachments=attachments or [],
        deleted_attachments=deleted_attachments or [],
        edited_at=edited_at,
        commit=commit,
        request=request,
    )


def _create_post_edit_action(
    *,
    post: Post,
    user: Union["User", str],
    edit_reason: str | None,
    old_content: str,
    attachments: list[Attachment],
    deleted_attachments: list[Attachment],
    edited_at: datetime | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> PostEdit:
    if isinstance(user, str):
        user_obj = None
        user_name = user
        user_slug = slugify(user)
    else:
        user_obj = user
        user_name = user.username
        user_slug = user.slug

    original_diff = diff_text(old_content, post.original)
    serialized_attachments, attachments_added, attachments_removed = (
        _serialize_attachments(attachments, deleted_attachments)
    )

    post_edit = PostEdit(
        category=post.category,
        thread=post.thread,
        post=post,
        user=user_obj,
        user_name=user_name,
        user_slug=user_slug,
        edit_reason=edit_reason,
        old_content=old_content,
        original_new=post.original,
        original_added=original_diff.added,
        original_removed=original_diff.removed,
        attachments=serialized_attachments,
        attachments_added=attachments_added,
        attachments_removed=attachments_removed,
        edited_at=edited_at,
    )

    if commit:
        post_edit.save()

    return post_edit


def _serialize_attachments(
    attachments: list[Attachment],
    deleted_attachments: list[Attachment],
) -> tuple[list[dict], int, int]:
    if not attachments and not deleted_attachments:
        return [], 0, 0

    new_attachments_ids = set(
        attachment.id for attachment in attachments if not attachment.post_id
    )
    deleted_attachments_ids = set(attachment.id for attachment in deleted_attachments)

    serialized_attachments = []
    for attachment in attachments + deleted_attachments:
        if attachment.id in new_attachments_ids:
            change = "+"
        elif attachment.id in deleted_attachments_ids:
            change = "-"
        else:
            change = "="

        serialized_attachments.append(
            {
                "id": attachment.id,
                "uploader": attachment.uploader_id,
                "uploader_name": attachment.uploader_name,
                "uploader_slug": attachment.uploader_slug,
                "uploaded_at": attachment.uploaded_at.isoformat(),
                "name": attachment.name,
                "filetype_id": attachment.filetype_id,
                "dimensions": attachment.dimensions,
                "size": attachment.size,
                "change": change,
            }
        )

    serialized_attachments = sorted(
        serialized_attachments, key=lambda a: a["id"], reverse=True
    )

    return (
        serialized_attachments,
        len(new_attachments_ids),
        len(deleted_attachments_ids),
    )
