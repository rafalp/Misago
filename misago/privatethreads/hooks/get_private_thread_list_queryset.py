from typing import Protocol

from django.http import HttpRequest
from django.db.models import QuerySet

from ...categories.models import Category
from ...plugins.hooks import FilterHook


class GetPrivateThreadListQuerysetHookAction(Protocol):
    """
    Misago function used to get the base threads queryset for
    the private thread list view.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    The private threads category instance.

    # Return value

    A `QuerySet` instance that will return `Threads`.
    """

    def __call__(self, request: HttpRequest, category: Category) -> QuerySet: ...


class GetPrivateThreadListQuerysetHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetPrivateThreadListQuerysetHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    The private threads category instance.

    # Return value

    A `QuerySet` instance that will return `Threads`.
    """

    def __call__(
        self,
        action: GetPrivateThreadListQuerysetHookAction,
        request: HttpRequest,
        category: Category,
    ) -> QuerySet: ...


class GetPrivateThreadListQuerysetHook(
    FilterHook[
        GetPrivateThreadListQuerysetHookAction,
        GetPrivateThreadListQuerysetHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get
    the base threads queryset for the private thread list view.

    # Example

    The code below implements a custom filter function that joins first post to
    every returned thread.

    ```python
    from django.db.models import QuerySet
    from django.http import HttpRequest
    from misago.categories.models import Category
    from misago.privatethreads.hooks import get_private_thread_list_queryset_hook


    @get_private_thread_list_queryset_hook.append_filter
    def select_first_post(action, request: HttpRequest) -> QuerySet:
        queryset = action(request)
        return queryset.select_related("first_post")
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetPrivateThreadListQuerysetHookAction,
        request: HttpRequest,
        category: Category,
    ) -> QuerySet:
        return super().__call__(action, request, category)


get_private_thread_list_queryset_hook = GetPrivateThreadListQuerysetHook(cache=False)
