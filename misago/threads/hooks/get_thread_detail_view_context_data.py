from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Thread


class GetThreadDetailViewContextDataHookAction(Protocol):
    """
    Misago function used to get the template context data
    for the thread detail view.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    A `Thread` instance.

    ## `page: int | None`

    An `int` with page number or `None`.

    ## `kwargs: dict`

    A Python `dict` with view's keyword arguments.

    # Return value

    A Python `dict` with context data to use to `render` the thread detail view.
    """

    def __call__(
        self,
        request: HttpRequest,
        thread: Thread,
        page: int | None,
        kwargs: dict,
    ) -> dict: ...


class GetThreadDetailViewContextDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadDetailViewContextDataHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    A `Thread` instance.

    ## `page: int | None = None`

    An `int` with page number or `None`.

    ## `kwargs: dict`

    A Python `dict` with view's keyword arguments.

    # Return value

    A Python `dict` with context data to use to `render` the thread detail view.
    """

    def __call__(
        self,
        action: GetThreadDetailViewContextDataHookAction,
        request: HttpRequest,
        thread: Thread,
        page: int | None,
        kwargs: dict,
    ) -> dict: ...


class GetThreadDetailViewContextDataHook(
    FilterHook[
        GetThreadDetailViewContextDataHookAction,
        GetThreadDetailViewContextDataHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get
    the template context data for the thread detail view.

    # Example

    The code below implements a custom filter function that adds custom context
    data to the thread detail view:

    ```python
    from django.http import HttpRequest
    from misago.threads.hooks import get_thread_detail_view_context_data_hook
    from misago.threads.models import Thread


    @get_thread_detail_view_context_data_hook.append_filter
    def include_custom_context(
        action,
        request: HttpRequest,
        thread: dict,
        page: int | None,
        kwargs: dict,
    ) -> dict:
        context = action(request, thread, page, kwargs)

        context["plugin_data"] = "..."

        return context
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadDetailViewContextDataHookAction,
        request: HttpRequest,
        thread: Thread,
        page: int | None,
        kwargs: dict,
    ) -> dict:
        return super().__call__(action, request, thread, page, kwargs)


get_thread_detail_view_context_data_hook = GetThreadDetailViewContextDataHook(
    cache=False
)
