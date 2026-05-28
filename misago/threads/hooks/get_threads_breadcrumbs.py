from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook


class GetThreadsBreadcrumbsHookAction(Protocol):
    """
    Misago function for retrieving the breadcrumbs for the threads list.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    # Return value

    A `dict` with a breadcrumbs template component.
    """

    def __call__(self, request: HttpRequest) -> dict: ...


class GetThreadsBreadcrumbsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadsBreadcrumbsHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    # Return value

    A `dict` with a breadcrumbs template component.
    """

    def __call__(
        self,
        action: GetThreadsBreadcrumbsHookAction,
        request: HttpRequest,
    ) -> dict: ...


class GetThreadsBreadcrumbsHook(
    FilterHook[
        GetThreadsBreadcrumbsHookAction,
        GetThreadsBreadcrumbsHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    retrieve the breadcrumbs for the threads list.

    # Example

    Change the icon used for the threads list breadcrumb:

    ```python
    from django.http import HttpRequest
    from misago.threads.hooks import get_threads_breadcrumbs_hook


    @get_threads_breadcrumbs_hook.append_filter
    def set_threads_breadcrumb_icon(
        action, request: HttpRequest
    ) -> dict:
        breadcrumbs = action(request)
        breadcrumbs["items"][-1]["icon"] = "tabler/lock.svg"
        return breadcrumbs
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadsBreadcrumbsHookAction,
        request: HttpRequest,
    ) -> dict:
        return super().__call__(action, request)


get_threads_breadcrumbs_hook = GetThreadsBreadcrumbsHook()
