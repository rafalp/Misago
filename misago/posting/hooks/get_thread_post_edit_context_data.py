from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Post

if TYPE_CHECKING:
    from ..formsets import EditThreadPostFormset


class GetThreadPostEditContextDataHookAction(Protocol):
    """
    Misago function used to get the template context data for
    the thread post edit view.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    ## `formset: EditThreadPostFormset`

    The `EditThreadPostFormset` instance.

    # Return value

    A Python `dict` with context data used to `render` the thread post edit view.
    """

    def __call__(
        self,
        request: HttpRequest,
        post: Post,
        formset: "EditThreadPostFormset",
    ) -> dict: ...


class GetThreadPostEditContextDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadPostEditContextDataHookAction`

    The next function registered in this hook, either a custom function or
    Misago's default.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    ## `formset: EditThreadPostFormset`

    The `EditThreadPostFormset` instance.

    # Return value

    A Python `dict` with context data used to `render` the thread post edit view.
    """

    def __call__(
        self,
        action: GetThreadPostEditContextDataHookAction,
        request: HttpRequest,
        post: Post,
        formset: "EditThreadPostFormset",
    ) -> dict: ...


class GetThreadPostEditContextDataHook(
    FilterHook[
        GetThreadPostEditContextDataHookAction,
        GetThreadPostEditContextDataHookFilter,
    ]
):
    """
    This hook wraps the function Misago uses to get the template context data
    for the thread post edit view.

    # Example

    The code below implements a custom filter function that adds extra values to
    the template context data:

    ```python
    from django.http import HttpRequest
    from misago.posting.formsets import EditThreadPostFormset
    from misago.posting.hooks import get_thread_post_edit_context_data_hook
    from misago.threads.models import Post

    @get_thread_post_edit_context_data_hook.append_filter
    def set_show_first_post_warning_in_context(
        action,
        request: HttpRequest,
        post: Post,
        formset: EditThreadPostFormset,
    ) -> dict:
        context = action(request, thread, formset)
        context["show_first_post_warning"] = request.user.posts == 1
        return context
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadPostEditContextDataHookAction,
        request: HttpRequest,
        post: Post,
        formset: "EditThreadPostFormset",
    ) -> dict:
        return super().__call__(action, request, post, formset)


get_thread_post_edit_context_data_hook = GetThreadPostEditContextDataHook(cache=False)
