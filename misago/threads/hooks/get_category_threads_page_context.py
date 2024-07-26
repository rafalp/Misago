from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook


class GetCategoryThreadsPageContextHookAction(Protocol):
    """
    A standard Misago function used to get the template context
    for the category threads page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `kwargs: dict`

    A Python `dict` with view's keyword arguments.

    # Return value

    A Python `dict` with context to use to `render` the category threads page.
    """

    def __call__(self, request: HttpRequest, kwargs: dict) -> dict: ...


class GetCategoryThreadsPageContextHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetCategoryThreadsPageContextHookAction`

    A standard Misago function used to get the template context
    for the category threads page.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `kwargs: dict`

    A Python `dict` with view's keyword arguments.

    # Return value

    A Python `dict` with context to use to `render` the category threads page.
    """

    def __call__(
        self,
        action: GetCategoryThreadsPageContextHookAction,
        request: HttpRequest,
        kwargs: dict,
    ) -> dict: ...


class GetCategoryThreadsPageContextHook(
    FilterHook[
        GetCategoryThreadsPageContextHookAction,
        GetCategoryThreadsPageContextHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get
    the template for the category threads page.

    # Example

    The code below implements a custom filter function that adds custom context
    to the category threads page:

    ```python
    from django.http import HttpRequest
    from misago.threads.hooks import get_category_threads_page_context_hook


    @get_category_threads_page_context_hook.append_filter
    def include_custom_context(action, request: HttpRequest, kwargs: dict) -> dict:
        context = action(request, kwargs)

        context["plugin_data"] = "..."

        return context
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetCategoryThreadsPageContextHookAction,
        request: HttpRequest,
        kwargs: dict,
    ) -> dict:
        return super().__call__(action, request, kwargs)


get_category_threads_page_context_hook = GetCategoryThreadsPageContextHook()
