from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Thread


class GetThreadBreadcrumbsHookAction(Protocol):
    """
    Misago function for retrieving a private thread's breadcrumbs.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    The `Thread` to retrieve breadcrumbs for.

    # Return value

    A list of `dict`s representing the private thread's breadcrumbs.
    """

    def __call__(
        self,
        request: HttpRequest,
        thread: Thread,
    ) -> list[dict]: ...


class GetThreadBreadcrumbsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadBreadcrumbsHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    The `Thread` to retrieve breadcrumbs for.

    # Return value

    A list of `dict`s representing the private thread's breadcrumbs.
    """

    def __call__(
        self,
        action: GetThreadBreadcrumbsHookAction,
        request: HttpRequest,
        thread: Thread,
    ) -> list[dict]: ...


class GetThreadBreadcrumbsHook(
    FilterHook[
        GetThreadBreadcrumbsHookAction,
        GetThreadBreadcrumbsHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    retrieve a private thread's breadcrumbs.

    # Example

    Include extra data in a private thread's breadcrumbs:

    ```python
    from django.http import HttpRequest
    from misago.privatethreads.hooks import get_private_thread_breadcrumbs_hook
    from misago.threads.models import Thread


    @get_private_thread_breadcrumbs_hook.append_filter
    def set_private_thread_breadcrumb_icon(
        action, request: HttpRequest, thread: Thread
    ) -> list[dict]:
        breadcrumbs = action(request, thread)
        if thread.is_locked:
            breadcrumbs[-1]["icon"] = "tabler/lock.svg"
        return breadcrumbs
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadBreadcrumbsHookAction,
        request: HttpRequest,
        thread: Thread,
    ) -> list[dict]:
        return super().__call__(action, request, thread)


get_private_thread_breadcrumbs_hook = GetThreadBreadcrumbsHook()
