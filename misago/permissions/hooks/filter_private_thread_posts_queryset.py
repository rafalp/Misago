from typing import TYPE_CHECKING, Protocol

from django.db.models import QuerySet

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class FilterPrivateThreadPostsQuerysetHookAction(Protocol):
    """
    Misago function used to set filters on a queryset used to retrieve
    specified private thread's posts that user can see.

    # Arguments

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `thread: Thread`

    A private thread instance which's posts are retrieved.

    ## `queryset: Queryset`

    A queryset returning thread's posts.

    ## Return value

    A `queryset` filtered to show only thread posts that the user can see.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        thread: Thread,
        queryset: QuerySet,
    ) -> QuerySet: ...


class FilterPrivateThreadPostsQuerysetHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: FilterPrivateThreadPostsQuerysetHookAction`

    Misago function used to set filters on a queryset used to retrieve
    specified private thread's posts that user can see.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `thread: Thread`

    A private thread instance which's posts are retrieved.

    ## `queryset: Queryset`

    A queryset returning thread's posts.

    ## Return value

    A `queryset` filtered to show only thread posts that the user can see.
    """

    def __call__(
        self,
        action: FilterPrivateThreadPostsQuerysetHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
        queryset: QuerySet,
    ) -> QuerySet: ...


class FilterPrivateThreadPostsQuerysetHook(
    FilterHook[
        FilterPrivateThreadPostsQuerysetHookAction,
        FilterPrivateThreadPostsQuerysetHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses set filters on private
    thread's posts queryset to limit it only to posts that the user can see.

    # Example

    The code below implements a custom filter function hides deleted posts from
    anonymous user.

    ```python
    from misago.permissions.hooks import filter_private_thread_posts_queryset_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @filter_private_thread_posts_queryset_hook.append_filter
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
        action: FilterPrivateThreadPostsQuerysetHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
        queryset: QuerySet,
    ) -> QuerySet:
        return super().__call__(action, permissions, thread, queryset)


filter_private_thread_posts_queryset_hook = FilterPrivateThreadPostsQuerysetHook()
