from typing import TYPE_CHECKING, Protocol, Union

from django.db.models import QuerySet

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ...categories.models import Category
    from ...categories.proxy import CategoryProxy
    from ..proxy import UserPermissionsProxy


class FilterThreadsQuerysetHookAction(Protocol):
    """
    Misago function used to filter a queryset to retrieve threads user can see.

    # Arguments

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `categories: list[Category|CategoryProxy]`

    A list of categories to retrieve threads for.

    ## `queryset: Queryset | None = None`

    A queryset to filter. If `None`, defaults to `Thread.objects`

    ## Return value

    A `QuerySet` filtered to return only threads that the user can see.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        categories: list[Union["Category", "CategoryProxy"]],
        queryset: QuerySet | None = None,
    ) -> QuerySet: ...


class FilterThreadsQuerysetHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: FilterThreadsQuerysetHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `categories: list[Category|CategoryProxy]`

    A list of categories to retrieve threads for.

    ## `queryset: Queryset | None = None`

    A queryset to filter. If `None`, defaults to `Post.objects`

    ## Return value

    A `QuerySet` filtered to return only threads that the user can see.
    """

    def __call__(
        self,
        action: FilterThreadsQuerysetHookAction,
        permissions: "UserPermissionsProxy",
        categories: list[Union["Category", "CategoryProxy"]],
        queryset: QuerySet | None = None,
    ) -> QuerySet: ...


class FilterThreadsQuerysetHook(
    FilterHook[
        FilterThreadsQuerysetHookAction,
        FilterThreadsQuerysetHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to filter a queryset
    to retrieve threads user can see.

    This function is usually combined with the filter_threads_queryset
    to retrieve all threads the user can see from visible threads, e.g. for search
    results or user activity feeds.

    # Example

    The code below implements a custom filter function that hides too old threads
    from anonymous user.

    ```python
    from datetime import timedetla

    from django.db.models import QuerySet
    from django.utils import timezone
    from misago.categories.models import Category
    from misago.categories.proxy import CategoryProxy
    from misago.permissions.hooks import filter_threads_queryset_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @filter_threads_queryset_hook.append_filter
    def exclude_old_threads(
        action,
        permissions: UserPermissionsProxy,
        categories: list[Category | CategoryProxy]
        queryset: QuerySet | None = None,
    ) -> Queryset:
        queryset = action(permissions, categories, queryset)

        if permissions.user.is_anonymous:
            return queryset.filter(
                posted_at__gt=timezone.now() - timedelta(days=7)
            )

        return queryset
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: FilterThreadsQuerysetHookAction,
        permissions: "UserPermissionsProxy",
        categories: list[Union["Category", "CategoryProxy"]],
        queryset: QuerySet | None = None,
    ) -> QuerySet:
        return super().__call__(action, permissions, categories, queryset)


filter_threads_queryset_hook = FilterThreadsQuerysetHook()
