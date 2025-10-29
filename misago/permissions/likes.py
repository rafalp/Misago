from ..categories.models import Category
from ..threads.models import Post, Thread
from .hooks import (
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
    pass


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
    pass


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
    pass
