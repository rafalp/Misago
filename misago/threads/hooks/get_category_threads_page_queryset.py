from typing import Protocol

from django.http import HttpRequest
from django.db.models import QuerySet

from ...plugins.hooks import FilterHook


class GetCategoryThreadsPageQuerysetHookAction(Protocol):
    """
    A standard Misago function used to get the base threads queryset
    for the category threads page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    # Return value

    A `QuerySet` instance that will return `Threads`.
    """

    def __call__(self, request: HttpRequest) -> QuerySet: ...


class GetCategoryThreadsPageQuerysetHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetCategoryThreadsPageQuerysetHookAction`

    A standard Misago function used to get the base threads queryset
    for the category threads page.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    # Return value

    A `QuerySet` instance that will return `Threads`.
    """

    def __call__(
        self,
        action: GetCategoryThreadsPageQuerysetHookAction,
        request: HttpRequest,
    ) -> QuerySet: ...


class GetCategoryThreadsPageQuerysetHook(
    FilterHook[
        GetCategoryThreadsPageQuerysetHookAction,
        GetCategoryThreadsPageQuerysetHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get
    base threads queryset for the category threads page.

    # Example

    The code below implements a custom filter function that joins first post to
    every returned thread.

    ```python
    from django.db.models import QuerySet
    from django.http import HttpRequest
    from misago.threads.hooks import get_category_threads_page_queryset_hook


    @get_category_threads_page_queryset_hook.append_filter
    def select_first_post(action, request: HttpRequest) -> QuerySet:
        queryset = action(request)
        return queryset.select_related("first_post")
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetCategoryThreadsPageQuerysetHookAction,
        request: HttpRequest,
    ) -> QuerySet:
        return super().__call__(action, request)


get_category_threads_page_queryset_hook = GetCategoryThreadsPageQuerysetHook()
