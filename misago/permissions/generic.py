from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http import Http404

from ..categories.enums import CategoryTree
from ..categories.models import Category
from ..threads.models import Post, Thread
from .categories import check_see_category_permission
from .hooks import (
    check_access_category_permission_hook,
    check_access_post_permission_hook,
    check_access_thread_permission_hook,
    filter_accessible_thread_posts_hook,
)
from .privatethreads import (
    check_private_threads_permission,
    check_see_private_thread_permission,
    check_see_private_thread_post_permission,
    filter_private_thread_posts_queryset,
)
from .proxy import UserPermissionsProxy
from .threads import (
    check_see_thread_post_permission,
    check_see_thread_permission,
    filter_thread_posts_queryset,
)


def check_access_category_permission(
    permissions: UserPermissionsProxy, category: Category
):
    check_access_category_permission_hook(
        _check_access_category_permission_action, permissions, category
    )


def _check_access_category_permission_action(
    permissions: UserPermissionsProxy, category: Category
):
    if not category:
        raise Http404()

    if category.tree_id == CategoryTree.THREADS:
        check_see_category_permission(permissions, category)

    elif category.tree_id == CategoryTree.PRIVATE_THREADS:
        check_private_threads_permission(permissions)

    else:
        raise Http404()


def check_access_thread_permission(
    permissions: UserPermissionsProxy, category: Category, thread: Thread
):
    check_access_thread_permission_hook(
        _check_access_thread_permission_action, permissions, category, thread
    )


def _check_access_thread_permission_action(
    permissions: UserPermissionsProxy, category: Category, thread: Thread
):
    if not (category and thread):
        raise Http404()

    if category.tree_id == CategoryTree.THREADS:
        check_see_thread_permission(permissions, category, thread)

    elif category.tree_id == CategoryTree.PRIVATE_THREADS:
        try:
            check_private_threads_permission(permissions)
        except PermissionDenied:
            raise Http404()

        check_see_private_thread_permission(permissions, thread)

    else:
        raise Http404()


def check_access_post_permission(
    permissions: UserPermissionsProxy, category: Category, thread: Thread, post: Post
):
    check_access_post_permission_hook(
        _check_access_post_permission_action, permissions, category, thread, post
    )


def _check_access_post_permission_action(
    permissions: UserPermissionsProxy, category: Category, thread: Thread, post: Post
):
    if not (category and thread and post):
        raise Http404()

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


def filter_accessible_thread_posts(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    queryset: QuerySet,
) -> QuerySet:
    return filter_accessible_thread_posts_hook(
        _filter_accessible_thread_posts_action,
        permissions,
        category,
        thread,
        queryset,
    )


def _filter_accessible_thread_posts_action(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    queryset: QuerySet,
) -> QuerySet:
    if category.tree_id == CategoryTree.THREADS:
        return filter_thread_posts_queryset(permissions, thread, queryset)

    elif category.tree_id == CategoryTree.PRIVATE_THREADS:
        return filter_private_thread_posts_queryset(permissions, thread, queryset)

    else:
        return queryset.empty()
