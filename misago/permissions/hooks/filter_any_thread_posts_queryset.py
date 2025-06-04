from typing import TYPE_CHECKING, Protocol

from django.db.models import QuerySet

from ...categories.models import Category
from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class FilterAnyThreadPostsQuerysetHookAction(Protocol):
    """
    A standard Misago function used to set filters on a queryset used to retrieve
    specified thread's posts that user can see.

    # Arguments

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category instance which's posts are retrieved.

    ## `thread: Thread`

    A thread instance which's posts are retrieved.

    ## `queryset: Queryset`

    A queryset returning thread's posts.

    ## Return value

    A `queryset` filtered to show only thread posts that the user can see.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
        queryset: QuerySet,
    ) -> QuerySet: ...


class FilterAnyThreadPostsQuerysetHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: FilterAnyThreadPostsQuerysetHookAction`

    A standard Misago function used to set filters on a queryset used to retrieve
    specified thread's posts that user can see.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category instance which's posts are retrieved.

    ## `thread: Thread`

    A thread instance which's posts are retrieved.

    ## `queryset: Queryset`

    A queryset returning thread's posts.

    ## Return value

    A `queryset` filtered to show only thread posts that the user can see.
    """

    def __call__(
        self,
        action: FilterAnyThreadPostsQuerysetHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
        queryset: QuerySet,
    ) -> QuerySet: ...


class FilterAnyThreadPostsQuerysetHook(
    FilterHook[
        FilterAnyThreadPostsQuerysetHookAction,
        FilterAnyThreadPostsQuerysetHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to set filters on a
    queryset with posts from a thread of any type (regular, private, or
    plugin-specified) to limit it only to posts that the user can see.

    # Example

    The code below implements a custom filter function hides deleted posts from
    anonymous user.

    ```python
    from misago.permissions.hooks import filter_any_thread_posts_queryset_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @filter_any_thread_posts_queryset_hook.append_filter
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
        action: FilterAnyThreadPostsQuerysetHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
        queryset: QuerySet,
    ) -> QuerySet:
        return super().__call__(action, permissions, category, thread, queryset)


filter_any_thread_posts_queryset_hook = FilterAnyThreadPostsQuerysetHook()
