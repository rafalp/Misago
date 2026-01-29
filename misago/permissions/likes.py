from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext

from ..categories.models import Category
from ..threads.models import Post, Thread
from .enums import CanSeePostLikes
from .hooks import (
    can_see_post_likes_count_hook,
    check_like_post_permission_hook,
    check_see_post_likes_permission_hook,
    check_unlike_post_permission_hook,
)
from .proxy import UserPermissionsProxy


def check_like_post_permission(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
):
    check_like_post_permission_hook(
        _check_like_post_permission_action, permissions, category, thread, post
    )


def _check_like_post_permission_action(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
):
    if not permissions.user.is_authenticated:
        raise PermissionDenied(
            pgettext(
                "likes permission error",
                "You can't like posts.",
            )
        )

    if not permissions.can_like_posts:
        raise PermissionDenied(
            pgettext(
                "post likes permission error",
                "You can't like this post.",
            )
        )


def check_unlike_post_permission(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
):
    check_unlike_post_permission_hook(
        _check_unlike_post_permission_action, permissions, category, thread, post
    )


def _check_unlike_post_permission_action(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
):
    if not permissions.user.is_authenticated:
        raise PermissionDenied(
            pgettext(
                "likes permission error",
                "You can't remove posts likes.",
            )
        )

    if not permissions.can_like_posts:
        raise PermissionDenied(
            pgettext(
                "likes permission error",
                "You can't remove your like from this post.",
            )
        )


def can_see_post_likes_count(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
) -> bool:
    return can_see_post_likes_count_hook(
        _can_see_post_likes_count_action, permissions, category, thread, post
    )


def _can_see_post_likes_count_action(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
) -> bool:
    is_user_post = permissions.user.id and permissions.user.id == post.poster_id

    return (is_user_post and permissions.can_see_own_post_likes) or (
        not is_user_post and permissions.can_see_others_post_likes
    )


def check_see_post_likes_permission(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
):
    check_see_post_likes_permission_hook(
        _check_see_post_likes_permission_action, permissions, category, thread, post
    )


def _check_see_post_likes_permission_action(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
):
    is_user_post = permissions.user.id and permissions.user.id == post.poster_id

    if (
        is_user_post and permissions.can_see_own_post_likes != CanSeePostLikes.USERS
    ) or (
        not is_user_post
        and permissions.can_see_others_post_likes != CanSeePostLikes.USERS
    ):
        raise PermissionDenied(
            pgettext(
                "likes permission error",
                "You can't see this post's likes.",
            )
        )
