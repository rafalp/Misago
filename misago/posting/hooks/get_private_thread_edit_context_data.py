from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Post

if TYPE_CHECKING:
    from ..formsets import EditPrivateThreadFormset


class GetPrivateThreadEditContextDataHookAction(Protocol):
    """
    Misago function used to get the template context data for the thread edit view.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    ## `formset: EditPrivateThreadFormset`

    The `EditPrivateThreadFormset` instance.

    # Return value

    A Python `dict` with context data used to `render` the private thread edit view.
    """

    def __call__(
        self,
        request: HttpRequest,
        post: Post,
        formset: "EditPrivateThreadFormset",
    ) -> dict: ...


class GetPrivateThreadEditContextDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetPrivateThreadEditContextDataHookAction`

    The next function registered in this hook, either a custom function or
    Misago's default.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    ## `formset: EditPrivateThreadFormset`

    The `EditPrivateThreadFormset` instance.

    # Return value

    A Python `dict` with context data used to `render` the private thread edit view.
    """

    def __call__(
        self,
        action: GetPrivateThreadEditContextDataHookAction,
        request: HttpRequest,
        post: Post,
        formset: "EditPrivateThreadFormset",
    ) -> dict: ...


class GetPrivateThreadEditContextDataHook(
    FilterHook[
        GetPrivateThreadEditContextDataHookAction,
        GetPrivateThreadEditContextDataHookFilter,
    ]
):
    """
    This hook wraps the function Misago uses to get the template context data
    for the private thread edit view.

    # Example

    The code below implements a custom filter function that adds extra values to
    the template context data:

    ```python
    from django.http import HttpRequest
    from misago.posting.formsets import EditPrivateThreadFormset
    from misago.posting.hooks import get_private_thread_edit_context_data_hook
    from misago.threads.models import Post

    @get_private_thread_edit_context_data_hook.append_filter
    def set_show_first_post_warning_in_context(
        action,
        request: HttpRequest,
        post: Post,
        formset: EditPrivateThreadFormset,
    ) -> dict:
        context = action(request, thread, formset)
        context["show_first_post_warning"] = request.user.posts == 1
        return context
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetPrivateThreadEditContextDataHookAction,
        request: HttpRequest,
        post: Post,
        formset: "EditPrivateThreadFormset",
    ) -> dict:
        return super().__call__(action, request, post, formset)


get_private_thread_edit_context_data_hook = GetPrivateThreadEditContextDataHook(
    cache=False
)
