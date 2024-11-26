from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Post

if TYPE_CHECKING:
    from ...posting.formsets import EditPrivateThreadPostFormset


class GetEditPrivateThreadPostPageContextDataHookAction(Protocol):
    """
    A standard Misago function used to get the template context data
    for the edit private thread post page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    ## `formset: EditPrivateThreadPostFormset`

    The `EditPrivateThreadPostFormset` instance.

    # Return value

    A Python `dict` with context data to use to `render`
    the edit private thread post page.
    """

    def __call__(
        self,
        request: HttpRequest,
        post: Post,
        formset: "EditPrivateThreadPostFormset",
    ) -> dict: ...


class GetEditPrivateThreadPostPageContextDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetEditPrivateThreadPostPageContextDataHookAction`

    A standard Misago function used to get the template context data
    for the edit private thread post page.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    ## `formset: EditPrivateThreadPostFormset`

    The `EditPrivateThreadPostFormset` instance.

    # Return value

    A Python `dict` with context data to use to `render`
    the edit private thread post page.
    """

    def __call__(
        self,
        action: GetEditPrivateThreadPostPageContextDataHookAction,
        request: HttpRequest,
        post: Post,
        formset: "EditPrivateThreadPostFormset",
    ) -> dict: ...


class GetEditPrivateThreadPostPageContextDataHook(
    FilterHook[
        GetEditPrivateThreadPostPageContextDataHookAction,
        GetEditPrivateThreadPostPageContextDataHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get the template
    context data for the edit private thread post page.

    # Example

    The code below implements a custom filter function that adds extra values to
    the template context data:

    ```python
    from django.http import HttpRequest
    from misago.posting.formsets import EditPrivateThreadPostFormset
    from misago.threads.hooks import get_edit_private_thread_post_page_context_data_hook
    from misago.threads.models import Thread


    @get_edit_private_thread_post_page_context_data_hook.append_filter
    def set_show_first_post_warning_in_context(
        action,
        request: HttpRequest,
        post: Post,
        formset: EditPrivateThreadPostFormset,
    ) -> dict:
        context = action(request, thread, formset)
        context["show_first_post_warning"] = request.user.posts == 1
        return context
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetEditPrivateThreadPostPageContextDataHookAction,
        request: HttpRequest,
        post: Post,
        formset: "EditPrivateThreadPostFormset",
    ) -> dict:
        return super().__call__(action, request, post, formset)


get_edit_private_thread_post_page_context_data_hook = (
    GetEditPrivateThreadPostPageContextDataHook(cache=False)
)
