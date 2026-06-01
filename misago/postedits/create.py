from datetime import datetime
from typing import TYPE_CHECKING, Union

from django.http import HttpRequest
from django.utils import timezone

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
    edit_reason: str | None = None,
    old_title: str | None = None,
    new_title: str | None = None,
    old_content: str | None = None,
    new_content: str | None = None,
    attachments: list[Attachment] | None = None,
    deleted_attachments: list[Attachment] | None = None,
    edited_at: datetime | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> PostEdit:
    if old_title == new_title:
        old_title = new_title = None
    if old_content == new_content:
        old_content = new_content = None

    return create_post_edit_hook(
        _create_post_edit_action,
        post=post,
        user=user,
        edit_reason=edit_reason or None,
        old_title=old_title or None,
        new_title=new_title or None,
        old_content=old_content or None,
        new_content=new_content or None,
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
    old_title: str | None,
    new_title: str | None,
    old_content: str | None,
    new_content: str | None,
    attachments: list[Attachment],
    deleted_attachments: list[Attachment],
    edited_at: datetime | None,
    commit: bool = True,
    request: HttpRequest | None,
) -> PostEdit:
    if isinstance(user, str):
        user_obj = None
        user_name = user
        user_slug = slugify(user)
    else:
        user_obj = user
        user_name = user.username
        user_slug = user.slug

    if old_content and new_content:
        content_diff = diff_text(old_content, post.original)
        added_content = content_diff.added
        removed_content = content_diff.removed
    else:
        added_content = 0
        removed_content = 0

    serialized_attachments, added_attachments, removed_attachments = (
        _serialize_attachments(attachments, deleted_attachments)
    )

    if not edited_at:
        edited_at = timezone.now()

    post_edit = PostEdit(
        category=post.category,
        thread=post.thread,
        post=post,
        user=user_obj,
        user_name=user_name,
        user_slug=user_slug,
        edit_reason=edit_reason,
        old_title=old_title,
        new_title=new_title,
        old_content=old_content,
        new_content=new_content,
        added_content=added_content,
        removed_content=removed_content,
        attachments=serialized_attachments,
        added_attachments=added_attachments,
        removed_attachments=removed_attachments,
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

    # Exclude temporary deleted attachments from diff
    deleted_attachments = list(filter(lambda a: a.post_id, deleted_attachments))
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
                "uploader_id": attachment.uploader_id,
                "uploader_name": attachment.uploader_name,
                "uploader_slug": attachment.uploader_slug,
                "uploaded_at": attachment.uploaded_at.isoformat(),
                "name": attachment.name,
                "slug": attachment.slug,
                "filetype_id": attachment.filetype_id,
                "dimensions": _serialize_attachment_dimensions(attachment.dimensions),
                "thumbnail": _serialize_attachment_dimensions(
                    attachment.thumbnail_dimensions
                ),
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


def _serialize_attachment_dimensions(dimensions: str | None) -> list[int, int] | None:
    if not dimensions:
        return None
    return [int(size) for size in dimensions.split("x")]
