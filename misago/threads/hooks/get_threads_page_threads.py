from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook


class GetThreadsPageThreadsHookAction(Protocol):
    """
    A standard Misago function used to get the complete threads data for the threads page.
    Returns a `dict` that is included in the template context under the `threads` key.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `kwargs: dict`

    A `dict` with `kwargs` this view was called with.

    # Return value

    A `dict` with the template context.
    """

    def __call__(self, request: HttpRequest, kwargs: dict) -> dict: ...


class GetThreadsPageThreadsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadsPageThreadsHookAction`

    A standard Misago function used to get the complete threads data for the threads page.
    Returns a `dict` that is included in the template context under the `threads` key.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `kwargs: dict`

    A `dict` with `kwargs` this view was called with.

    # Return value

    A `dict` with the template context.
    """

    def __call__(
        self,
        action: GetThreadsPageThreadsHookAction,
        request: HttpRequest,
        kwargs: dict,
    ) -> dict: ...


class GetThreadsPageThreadsHook(
    FilterHook[
        GetThreadsPageThreadsHookAction,
        GetThreadsPageThreadsHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get
    complete threads data for the threads page.

    # Example

    The code below implements a custom filter function makes view use a different
    threads list template instead of the default one.

    ```python
    from django.http import HttpRequest
    from misago.threads.hooks import get_threads_page_threads_hook


    @get_threads_page_threads_hook.append_filter
    def replace_threads_list_template(
        action, request: HttpRequest, kwargs: dict
    ) -> dict:
        data = action(request, kwargs)
        data["template_name"] = "plugin/threads_list.html"
        return data
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadsPageThreadsHookAction,
        request: HttpRequest,
        kwargs: dict,
    ) -> dict:
        return super().__call__(action, request, kwargs)


get_threads_page_threads_hook = GetThreadsPageThreadsHook(cache=False)
