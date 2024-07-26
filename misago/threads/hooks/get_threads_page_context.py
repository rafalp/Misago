from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook


class GetThreadsPageContextHookAction(Protocol):
    """
    A standard Misago function used to get the template context
    for the threads page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `kwargs: dict`

    A Python `dict` with view's keyword arguments.

    # Return value

    A Python `dict` with context to use to `render` the threads page.
    """

    def __call__(self, request: HttpRequest, kwargs: dict) -> dict: ...


class GetThreadsPageContextHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadsPageContextHookAction`

    A standard Misago function used to get the template context
    for the threads page.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `kwargs: dict`

    A Python `dict` with view's keyword arguments.

    # Return value

    A Python `dict` with context to use to `render` the threads page.
    """

    def __call__(
        self,
        action: GetThreadsPageContextHookAction,
        request: HttpRequest,
        kwargs: dict,
    ) -> dict: ...


class GetThreadsPageContextHook(
    FilterHook[
        GetThreadsPageContextHookAction,
        GetThreadsPageContextHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get
    the template for the threads page.

    # Example

    The code below implements a custom filter function that adds custom context
    to the threads page:

    ```python
    from django.http import HttpRequest
    from misago.threads.hooks import get_threads_page_context_hook


    @get_threads_page_context_hook.append_filter
    def include_custom_context(action, request: HttpRequest, kwargs: dict) -> dict:
        context = action(request, kwargs)

        context["plugin_data"] = "..."

        return context
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadsPageContextHookAction,
        request: HttpRequest,
        kwargs: dict,
    ) -> dict:
        return super().__call__(action, request, kwargs)


get_threads_page_context_hook = GetThreadsPageContextHook()
