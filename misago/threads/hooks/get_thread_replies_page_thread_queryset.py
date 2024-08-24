from typing import Protocol

from django.db.models import QuerySet
from django.http import HttpRequest

from ...plugins.hooks import FilterHook


class GetThreadRepliesPageThreadQuerysetHookAction(Protocol):
    """
    A standard Misago function used to get a queryset used to get a thread for
    the thread replies page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    # Return value

    A `QuerySet` instance to use in the `get_object_or_404` call.
    """

    def __call__(self, request: HttpRequest) -> QuerySet: ...


class GetThreadRepliesPageThreadQuerysetHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadRepliesPageThreadQuerysetHookAction`

    A standard Misago function used to get a queryset used to get a thread for
    the thread replies page.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    # Return value

    A `QuerySet` instance to use in the `get_object_or_404` call.
    """

    def __call__(
        self,
        action: GetThreadRepliesPageThreadQuerysetHookAction,
        request: HttpRequest,
    ) -> QuerySet: ...


class GetThreadRepliesPageThreadQuerysetHook(
    FilterHook[
        GetThreadRepliesPageThreadQuerysetHookAction,
        GetThreadRepliesPageThreadQuerysetHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get a queryset
    used to get a thread for the thread replies page.

    # Example

    The code below implements a custom filter function that joins plugin's table
    with `select_related`:

    ```python
    from django.http import HttpRequest
    from misago.threads.hooks import get_thread_replies_page_thread_queryset_hook


    @get_thread_replies_page_thread_queryset_hook.append_filter
    def select_related_plugin_data(action, request: HttpRequest):
        queryset = action(request)
        return queryset.select_related("plugin")
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadRepliesPageThreadQuerysetHookAction,
        request: HttpRequest,
    ) -> dict:
        return super().__call__(action, request)


get_thread_replies_page_thread_queryset_hook = GetThreadRepliesPageThreadQuerysetHook()
