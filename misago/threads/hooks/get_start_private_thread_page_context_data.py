from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...categories.models import Category
from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ...posting.formsets import StartPrivateThreadFormset


class GetStartPrivateThreadPageContextDataHookAction(Protocol):
    """
    A standard Misago function used to get the template context data
    for the start private thread page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    The `Category` instance.

    ## `formset: StartPrivateThreadFormset`

    The `StartPrivateThreadFormset` instance.

    # Return value

    A Python `dict` with context data to use to `render` the start private thread page.
    """

    def __call__(
        self,
        request: HttpRequest,
        category: Category,
        formset: "StartPrivateThreadFormset",
    ) -> dict: ...


class GetStartPrivateThreadPageContextDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetStartPrivateThreadPageContextDataHookAction`

    A standard Misago function used to get the template context data
    for the start private thread page.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    The `Category` instance.

    ## `formset: StartPrivateThreadFormset`

    The `StartPrivateThreadFormset` instance.

    # Return value

    A Python `dict` with context data to use to `render` the start private thread page.
    """

    def __call__(
        self,
        action: GetStartPrivateThreadPageContextDataHookAction,
        request: HttpRequest,
        category: Category,
        formset: "StartPrivateThreadFormset",
    ) -> dict: ...


class GetStartPrivateThreadPageContextDataHook(
    FilterHook[
        GetStartPrivateThreadPageContextDataHookAction,
        GetStartPrivateThreadPageContextDataHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get the template
    context data for the start private thread page.

    # Example

    The code below implements a custom filter function that adds extra values to
    the template context data:

    ```python
    from django.http import HttpRequest
    from misago.categories.models import Category
    from misago.posting.formsets import StartPrivateThreadFormset
    from misago.threads.hooks import get_start_private_thread_page_context_data_hook


    @get_start_private_thread_page_context_data_hook.append_filter
    def set_show_first_post_warning_in_context(
        action,
        request: HttpRequest,
        category: Category,
        formset: StartPrivateThreadFormset,
    ) -> dict:
        context = action(request, category, formset)
        context["show_first_post_warning"] = not request.user.posts
        return context
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetStartPrivateThreadPageContextDataHookAction,
        request: HttpRequest,
        category: Category,
        formset: "StartPrivateThreadFormset",
    ) -> dict:
        return super().__call__(action, request, category, formset)


get_start_private_thread_page_context_data_hook = (
    GetStartPrivateThreadPageContextDataHook(cache=False)
)
