from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...categories.models import Category
from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ...posting.formsets import StartThreadFormset


class GetStartThreadPageContextDataHookAction(Protocol):
    """
    A standard Misago function used to get the template context data
    for the start thread page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    The `Category` instance.

    ## `formset: StartThreadFormset`

    The `StartThreadFormset` instance.

    # Return value

    A Python `dict` with context data to use to `render` the start thread page.
    """

    def __call__(
        self,
        request: HttpRequest,
        category: Category,
        formset: "StartThreadFormset",
    ) -> dict: ...


class GetStartThreadPageContextDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetStartThreadPageContextDataHookAction`

    A standard Misago function used to get the template context data
    for the start thread page.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    The `Category` instance.

    ## `formset: StartThreadFormset`

    The `StartThreadFormset` instance.

    # Return value

    A Python `dict` with context data to use to `render` the start thread page.
    """

    def __call__(
        self,
        action: GetStartThreadPageContextDataHookAction,
        request: HttpRequest,
        category: Category,
        formset: "StartThreadFormset",
    ) -> dict: ...


class GetStartThreadPageContextDataHook(
    FilterHook[
        GetStartThreadPageContextDataHookAction, GetStartThreadPageContextDataHookFilter
    ]
):
    """
    This hook wraps the standard function that Misago uses to get the template
    context data for the start thread page.

    # Example

    The code below implements a custom filter function that adds extra values to
    the template context data:

    ```python
    from django.http import HttpRequest
    from misago.categories.models import Category
    from misago.posting.formsets import StartThreadFormset
    from misago.threads.hooks import get_start_thread_page_context_data_hook


    @get_start_thread_page_context_data_hook.append_filter
    def set_show_first_post_warning_in_context(
        action,
        request: HttpRequest,
        category: Category,
        formset: StartThreadFormset,
    ) -> dict:
        context = action(request, category, formset)
        context["show_first_post_warning"] = not request.user.posts
        return context
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetStartThreadPageContextDataHookAction,
        request: HttpRequest,
        category: Category,
        formset: "StartThreadFormset",
    ) -> dict:
        return super().__call__(action, request, category, formset)


get_start_thread_page_context_data_hook = GetStartThreadPageContextDataHook(cache=False)
