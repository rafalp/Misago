from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook


class GetPrivateThreadListContextDataHookAction(Protocol):
    """
    Misago function used to get the template context data for
    the private thread list view.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `kwargs: dict`

    A Python `dict` with view's keyword arguments.

    # Return value

    A Python `dict` with context data to use to `render` the private threads page.
    """

    def __call__(self, request: HttpRequest, kwargs: dict) -> dict: ...


class GetPrivateThreadListContextDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetPrivateThreadListContextDataHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

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
        action: GetPrivateThreadListContextDataHookAction,
        request: HttpRequest,
        kwargs: dict,
    ) -> dict: ...


class GetPrivateThreadListContextDataHook(
    FilterHook[
        GetPrivateThreadListContextDataHookAction,
        GetPrivateThreadListContextDataHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get
    the template context data for the private thread list view.

    # Example

    The code below implements a custom filter function that adds extra values to
    the template context data:

    ```python
    from django.http import HttpRequest
    from misago.privatethreads.hooks import get_private_thread_list_context_data_hook


    @get_private_thread_list_context_data_hook.append_filter
    def include_custom_context(action, request: HttpRequest, : dict) -> dict:
        context = action(request, kwargs)

        context["plugin_data"] = "..."

        return context
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetPrivateThreadListContextDataHookAction,
        request: HttpRequest,
        kwargs: dict,
    ) -> dict:
        return super().__call__(action, request, kwargs)


get_private_thread_list_context_data_hook = GetPrivateThreadListContextDataHook(
    cache=False
)
