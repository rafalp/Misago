from typing import TYPE_CHECKING, Protocol

from django.db.models import QuerySet

from ...categories.models import Category
from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class FilterAccessibleThreadPostsHookAction(Protocol):
    """
    Misago function used to set filters on a queryset of posts from
    a thread of any type (regular, private, or plugin-specified), limiting it
    to only the posts that the user can see.

    # Arguments

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category instance whose posts are being retrieved.

    ## `thread: Thread`

    A thread instance whose posts are being retrieved.

    ## `queryset: Queryset`

    A queryset returning the thread's posts.

    ## Return value

    A `QuerySet` filtered to return only the posts that the user can see.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
        queryset: QuerySet,
    ) -> QuerySet: ...


class FilterAccessibleThreadPostsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: FilterAccessibleThreadPostsHookAction`

    Misago function used to set filters on a queryset of posts from
    a thread of any type (regular, private, or plugin-specified), limiting it
    to only the posts that the user can see.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category instance whose posts are being retrieved.

    ## `thread: Thread`

    A thread instance whose posts are being retrieved.

    ## `queryset: Queryset`

    A queryset returning the thread's posts.

    ## Return value

    A `QuerySet` filtered to return only the posts that the user can see.
    """

    def __call__(
        self,
        action: FilterAccessibleThreadPostsHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
        queryset: QuerySet,
    ) -> QuerySet: ...


class FilterAccessibleThreadPostsHook(
    FilterHook[
        FilterAccessibleThreadPostsHookAction,
        FilterAccessibleThreadPostsHookFilter,
    ]
):
    """
    This hook wraps a standard Misago function used to set filters on a queryset
    of posts from   a thread of any type (regular, private, or plugin-specified),
    limiting it to only the posts that the user can see.

    # Example

    The code below implements a custom filter function removes hidden posts for
    anonymous user.

    ```python
    from misago.permissions.hooks import filter_accessible_thread_posts_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @filter_accessible_thread_posts_hook.append_filter
    def exclude_old_private_threads_queryset_hook(
        action,
        permissions: UserPermissionsProxy,
        thread,
        queryset,
    ) -> None:
        queryset = action(permissions, thread, queryset)

        if permissions.user.is_anonymous:
            return queryset.filter(is_hidden=False)

        return queryset
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: FilterAccessibleThreadPostsHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
        queryset: QuerySet,
    ) -> QuerySet:
        return super().__call__(action, permissions, category, thread, queryset)


filter_accessible_thread_posts_hook = FilterAccessibleThreadPostsHook()
