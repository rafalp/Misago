from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Thread


class GetPrivateThreadPostsViewContextDataHookAction(Protocol):
    """
    Misago function used to get the template context data
    for the private thread replies page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    A `Thread` instance.

    ## `page: int | None = None`

    An `int` with page number or `None`.

    # Return value

    A Python `dict` with context data to use to `render` the private thread
    replies page.
    """

    def __call__(
        self,
        request: HttpRequest,
        thread: Thread,
        page: int | None = None,
    ) -> dict: ...


class GetPrivateThreadPostsViewContextDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetPrivateThreadPostsViewContextDataHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    A `Thread` instance.

    ## `page: int | None = None`

    An `int` with page number or `None`.

    # Return value

    A Python `dict` with context data to use to `render` the private thread
    replies page.
    """

    def __call__(
        self,
        action: GetPrivateThreadPostsViewContextDataHookAction,
        request: HttpRequest,
        thread: Thread,
        page: int | None = None,
    ) -> dict: ...


class GetPrivateThreadPostsViewContextDataHook(
    FilterHook[
        GetPrivateThreadPostsViewContextDataHookAction,
        GetPrivateThreadPostsViewContextDataHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get
    the template context data for the private thread replies page.

    # Example

    The code below implements a custom filter function that adds custom context
    data to the thread replies page:

    ```python
    from django.http import HttpRequest
    from misago.privatethreads.hooks import get_private_thread_posts_view_context_data_hook
    from misago.threads.models import Thread


    @get_private_thread_posts_view_context_data_hook.append_filter
    def include_custom_context(
        action,
        request: HttpRequest,
        thread: dict,
        page: int | None = None,
    ) -> dict:
        context = action(request, thread, page)

        context["plugin_data"] = "..."

        return context
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetPrivateThreadPostsViewContextDataHookAction,
        request: HttpRequest,
        thread: Thread,
        page: int | None = None,
    ) -> dict:
        return super().__call__(action, request, thread, page)


get_private_thread_posts_view_context_data_hook = (
    GetPrivateThreadPostsViewContextDataHook(cache=False)
)
