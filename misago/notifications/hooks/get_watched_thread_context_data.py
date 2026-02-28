from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import WatchedThread


class GetWatchedThreadContextDataHookAction(Protocol):
    """
    Misago function used to get the template context data
    for the watch thread HTMX response.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `watched_thread: WatchedThread | None`

    The `WatchedThread` instance, or `None` if the thread is not watched.

    # Return value

    A Python `dict` with context data to use to render
    the watched thread HTMX response.
    """

    def __call__(
        self,
        request: HttpRequest,
        watched_thread: WatchedThread | None,
    ) -> dict: ...


class GetWatchedThreadContextDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetWatchedThreadContextDataHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `watched_thread: WatchedThread | None`

    The `WatchedThread` instance, or `None` if the thread is not watched.

    # Return value

    A Python `dict` with context data to use to render
    the watched thread HTMX response.
    """

    def __call__(
        self,
        action: GetWatchedThreadContextDataHookAction,
        request: HttpRequest,
        watched_thread: WatchedThread | None,
    ) -> dict: ...


class GetWatchedThreadContextDataHook(
    FilterHook[
        GetWatchedThreadContextDataHookAction,
        GetWatchedThreadContextDataHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get
    the template context data for the watch thread HTMX response.

    # Example

    Replace the template used to render the button's contents with a custom one:

    ```python
    from django.http import HttpRequest
    from misago.notifications.hooks import get_watched_thread_context_data_hook
    from misago.notifications.models import WatchedThread


    @get_watched_thread_context_data_hook.append_filter
    def change_watched_thread_button_template(
        action,
        request: HttpRequest,
        watched_thread: WatchedThread,
    )-> dict:
        context_data = action(request, watched_thread)
        context_data["button_template"] = "my_plugin/button.html"
        return context_data
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetWatchedThreadContextDataHookAction,
        request: HttpRequest,
        watched_thread: WatchedThread | None,
    ) -> dict:
        return super().__call__(
            action,
            request,
            watched_thread,
        )


get_watched_thread_context_data_hook = GetWatchedThreadContextDataHook()
