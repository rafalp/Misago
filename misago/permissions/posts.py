from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http import Http404

from ..categories.enums import CategoryTree
from ..categories.models import Category
from ..threads.models import Post, Thread
from .hooks import (
    filter_any_thread_posts_queryset_hook,
)
from .privatethreads import (
    filter_private_thread_posts_queryset,
)
from .proxy import UserPermissionsProxy
from .threads import (
    filter_thread_posts_queryset,
)


def filter_any_thread_posts_queryset(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    queryset: QuerySet,
) -> QuerySet:
    return filter_any_thread_posts_queryset_hook(
        _filter_any_thread_posts_queryset_action,
        permissions,
        category,
        thread,
        queryset,
    )


def _filter_any_thread_posts_queryset_action(
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
