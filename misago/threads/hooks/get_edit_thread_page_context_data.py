from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Post

if TYPE_CHECKING:
    from ...posting.formsets import EditThreadFormset


class GetEditThreadPostPageContextDataHookAction(Protocol):
    """
    Misago function used to get the template context data
    for the edit thread page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    ## `formset: EditThreadFormset`

    The `EditThreadFormset` instance.

    # Return value

    A Python `dict` with context data to use to `render`
    the edit thread page.
    """

    def __call__(
        self,
        request: HttpRequest,
        post: Post,
        formset: "EditThreadFormset",
    ) -> dict: ...


class GetEditThreadPostPageContextDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetEditThreadPostPageContextDataHookAction`

    Misago function used to get the template context data
    for the edit thread page.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    ## `formset: EditThreadFormset`

    The `EditThreadFormset` instance.

    # Return value

    A Python `dict` with context data to use to `render`
    the edit thread page.
    """

    def __call__(
        self,
        action: GetEditThreadPostPageContextDataHookAction,
        request: HttpRequest,
        post: Post,
        formset: "EditThreadFormset",
    ) -> dict: ...


class GetEditThreadPostPageContextDataHook(
    FilterHook[
        GetEditThreadPostPageContextDataHookAction,
        GetEditThreadPostPageContextDataHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get the template
    context data for the edit thread page.

    # Example

    The code below implements a custom filter function that adds extra values to
    the template context data:

    ```python
    from django.http import HttpRequest
    from misago.posting.formsets import EditThreadFormset
    from misago.threads.hooks import get_edit_thread_page_context_data_hook
    from misago.threads.models import Thread


    @get_edit_thread_page_context_data_hook.append_filter
    def set_show_first_post_warning_in_context(
        action,
        request: HttpRequest,
        post: Post,
        formset: EditThreadFormset,
    ) -> dict:
        context = action(request, thread, formset)
        context["show_first_post_warning"] = request.user.posts == 1
        return context
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetEditThreadPostPageContextDataHookAction,
        request: HttpRequest,
        post: Post,
        formset: "EditThreadFormset",
    ) -> dict:
        return super().__call__(action, request, post, formset)


get_edit_thread_page_context_data_hook = GetEditThreadPostPageContextDataHook(
    cache=False
)
