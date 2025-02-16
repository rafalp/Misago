from django.core.exceptions import PermissionDenied
from django.http import Http404

from ..categories.enums import CategoryTree
from ..categories.models import Category
from ..threads.models import Post, Thread
from .hooks import check_see_post_permission_hook
from .privatethreads import (
    check_private_threads_permission,
    check_see_private_thread_permission,
    check_see_private_thread_post_permission,
)
from .proxy import UserPermissionsProxy
from .threads import check_see_thread_post_permission, check_see_thread_permission


def check_see_post_permission(
    permissions: UserPermissionsProxy, category: Category, thread: Thread, post: Post
):
    check_see_post_permission_hook(
        _check_see_post_permission_action, permissions, category, thread, post
    )


def _check_see_post_permission_action(
    permissions: UserPermissionsProxy, category: Category, thread: Thread, post: Post
):
    if not (category and thread and post):
        raise Http404()  # Skip remaining permission checks

    if category.tree_id == CategoryTree.THREADS:
        try:
            check_see_thread_permission(permissions, category, thread)
        except PermissionDenied as exc:
            raise Http404() from exc

        check_see_thread_post_permission(permissions, category, thread, post)

    elif category.tree_id == CategoryTree.PRIVATE_THREADS:
        try:
            check_private_threads_permission(permissions)
            check_see_private_thread_permission(permissions, thread)
        except PermissionDenied:
            raise Http404()

        check_see_private_thread_post_permission(permissions, thread, post)

    else:
        raise Http404()
