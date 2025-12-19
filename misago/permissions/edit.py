from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext

from ..categories.models import Category
from ..threads.models import Post, Thread
from .enums import CanSeePostEdits
from .hooks import (
    can_see_post_edits_hook,
    check_see_post_edits_history_hook,
)
from .proxy import UserPermissionsProxy

def can_see_post_edits(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
) -> bool:
    return can_see_post_edits_hook(
        _can_see_post_edits_action, permissions, category, thread, post
    )


def _can_see_post_edits_action(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
) -> bool:
    is_user_post = permissions.user.id and permissions.user.id == post.poster_id
    return is_user_post or permissions.can_see_others_post_edits


def check_see_post_edits_history(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
):
    check_see_post_edits_history_hook(
        _check_see_post_edits_history_action, permissions, category, thread, post
    )


def _check_see_post_edits_history_action(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
):
    is_user_post = permissions.user.id and permissions.user.id == post.poster_id

    if (
        not is_user_post
        and permissions.can_see_others_post_edits != CanSeePostEdits.HISTORY
    ):
        raise PermissionDenied(
            pgettext(
                "edits permission error",
                "You can’t see this post’s edit history.",
            )
        )
