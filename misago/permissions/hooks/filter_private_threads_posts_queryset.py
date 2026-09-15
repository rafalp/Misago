from typing import TYPE_CHECKING, Protocol

from django.db.models import QuerySet

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class FilterPrivateThreadsPostsQuerysetHookAction(Protocol):
    """
    Misago function used to filter a queryset to retrieve private threads posts
    the user can see.

    # Arguments

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `queryset: Queryset`

    A queryset returning posts.

    ## Return value

    A `QuerySet` filtered to show only thread posts that the user can see.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        queryset: QuerySet,
    ) -> QuerySet: ...


class FilterPrivateThreadsPostsQuerysetHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: FilterPrivateThreadsPostsQuerysetHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `queryset: Queryset`

    A queryset returning posts.

    ## Return value

    A `QuerySet` filtered to show only thread posts that the user can see.
    """

    def __call__(
        self,
        action: FilterPrivateThreadsPostsQuerysetHookAction,
        permissions: "UserPermissionsProxy",
        queryset: QuerySet,
    ) -> QuerySet: ...


class FilterPrivateThreadsPostsQuerysetHook(
    FilterHook[
        FilterPrivateThreadsPostsQuerysetHookAction,
        FilterPrivateThreadsPostsQuerysetHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to filter a queryset
    to retrieve private threads posts the user can see.

    This function is usually combined with the `filter_private_threads_queryset`
    to retrieve all posts the user can see from visible threads, e.g. for search
    results.

    # Example

    The code below implements a custom filter function that hides too old posts
    from the user.

    ```python
    from datetime import timedetla

    from django.db.models import QuerySet
    from django.utils import timezone
    from misago.permissions.hooks import filter_private_threads_posts_queryset_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @filter_private_threads_posts_queryset_hook.append_filter
    def exclude_old_posts(
        action,
        permissions: UserPermissionsProxy,
        queryset: QuerySet | None = None,
    ) -> Queryset:
        queryset = action(permissions, queryset)

        if permissions.is_private_threads_moderator:
            return queryset

        return queryset.filter(
            posted_at__gt=timezone.now() - timedelta(days=7)
        )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: FilterPrivateThreadsPostsQuerysetHookAction,
        permissions: "UserPermissionsProxy",
        queryset: QuerySet,
    ) -> QuerySet:
        return super().__call__(action, permissions, queryset)


filter_private_threads_posts_queryset_hook = FilterPrivateThreadsPostsQuerysetHook()
