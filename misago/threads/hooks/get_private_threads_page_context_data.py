from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook


class GetPrivateThreadsPageContextDataHookAction(Protocol):
    """
    A standard Misago function used to get the template context data
    for the private threads page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `kwargs: dict`

    A Python `dict` with view's keyword arguments.

    # Return value

    A Python `dict` with context data to use to `render` the private threads page.
    """

    def __call__(self, request: HttpRequest, kwargs: dict) -> dict: ...


class GetPrivateThreadsPageContextDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetPrivateThreadsPageContextDataHookAction`

    A standard Misago function used to get the template context data
    for the private threads page.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `kwargs: dict`

    A Python `dict` with view's keyword arguments.

    # Return value

    A Python `dict` with context data to use to `render` the private threads page.
    """

    def __call__(
        self,
        action: GetPrivateThreadsPageContextDataHookAction,
        request: HttpRequest,
        kwargs: dict,
    ) -> dict: ...


class GetPrivateThreadsPageContextDataHook(
    FilterHook[
        GetPrivateThreadsPageContextDataHookAction,
        GetPrivateThreadsPageContextDataHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get
    the template context data for the private threads page.

    # Example

    The code below implements a custom filter function that adds custom context
    data to the private threads page:

    ```python
    from django.http import HttpRequest
    from misago.threads.hooks import get_private_threads_page_context_data_hook


    @get_private_threads_page_context_data_hook.append_filter
    def include_custom_context(action, request: HttpRequest, : dict) -> dict:
        context = action(request, kwargs)

        context["plugin_data"] = "..."

        return context
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetPrivateThreadsPageContextDataHookAction,
        request: HttpRequest,
        kwargs: dict,
    ) -> dict:
        return super().__call__(action, request, kwargs)


get_private_threads_page_context_data_hook = GetPrivateThreadsPageContextDataHook(
    cache=False
)
