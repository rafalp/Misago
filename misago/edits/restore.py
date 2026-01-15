from typing import TYPE_CHECKING, Union

from django.db.models import F
from django.http import HttpRequest
from django.utils import timezone

from ..attachments.models import Attachment
from ..core.utils import slugify
from ..parser.parse import parse
from ..posting.tasks import upgrade_post_content
from ..posting.upgradepost import post_needs_content_upgrade
from ..threads.models import Post
from .create import create_post_edit
from .hooks import restore_post_edit_hook
from .models import PostEdit

if TYPE_CHECKING:
    from ..users.models import User


def restore_post_edit(
    post_edit: PostEdit,
    user: Union["User", str],
    commit: bool = True,
    request: HttpRequest | None = None,
) -> tuple[Post, PostEdit]:
    return restore_post_edit_hook(
        _restore_post_edit_action, post_edit, user, commit, request
    )


def _restore_post_edit_action(
    post_edit: PostEdit,
    user: Union["User", str],
    commit: bool = True,
    request: HttpRequest | None = None,
) -> tuple[Post, PostEdit]:
    timestamp = timezone.now()
    post = post_edit.post
    old_content = post.original
    new_content = post_edit.old_content

    if isinstance(user, str):
        user_obj = None
        user_name = user
        user_slug = slugify(user)
    else:
        user_obj = user
        user_name = user.username
        user_slug = user.slug

    parsing_result = parse(new_content)

    post.original = parsing_result.markup
    post.parsed = parsing_result.html
    post.metadata = parsing_result.metadata
    post.set_search_document(post.thread)

    post.updated_at = timestamp
    post.edits = F("edits") + 1
    post.last_editor = user_obj
    post.last_editor_name = user_name
    post.last_editor_slug = user_slug
    post.last_edit_reason = None

    new_post_edit = create_post_edit(
        post=post,
        user=user,
        old_content=old_content,
        new_content=new_content,
        attachments=Attachment.objects.filter(post=post).order_by("-id"),
        edited_at=timestamp,
        request=request,
    )

    if commit:
        post.save()

        post.set_search_vector()
        post.save(update_fields=["search_vector"])

        new_post_edit.save()

        if post_needs_content_upgrade(post):
            upgrade_post_content.delay(post.id, post.sha256_checksum)

    return post, new_post_edit
