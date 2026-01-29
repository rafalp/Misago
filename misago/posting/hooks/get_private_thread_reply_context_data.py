from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..formsets import ReplyPrivateThreadFormset


class GetPrivateThreadReplyContextDataHookAction(Protocol):
    """
    Misago function used to get the template context data for
    the private thread reply view.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    The `Thread` instance.

    ## `formset: ReplyPrivateThreadFormset`

    The `ReplyPrivateThreadFormset` instance.

    # Return value

    A Python `dict` with context data used to `render`
    the private thread thread reply view.
    """

    def __call__(
        self,
        request: HttpRequest,
        thread: Thread,
        formset: "ReplyPrivateThreadFormset",
    ) -> dict: ...


class GetPrivateThreadReplyContextDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetPrivateThreadReplyContextDataHookAction`

    The next function registered in this hook, either a custom function or
    Misago's default.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    The `Thread` instance.

    ## `formset: ReplyPrivateThreadFormset`

    The `ReplyPrivateThreadFormset` instance.

    # Return value

    A Python `dict` with context data used to `render`
    the private thread thread reply view.
    """

    def __call__(
        self,
        action: GetPrivateThreadReplyContextDataHookAction,
        request: HttpRequest,
        thread: Thread,
        formset: "ReplyPrivateThreadFormset",
    ) -> dict: ...


class GetPrivateThreadReplyContextDataHook(
    FilterHook[
        GetPrivateThreadReplyContextDataHookAction,
        GetPrivateThreadReplyContextDataHookFilter,
    ]
):
    """
    This hook wraps the function Misago uses to get the template context data
    for the private thread reply view.

    # Example

    The code below implements a custom filter function that adds extra values to
    the template context data:

    ```python
    from django.http import HttpRequest
    from misago.posting.formsets import ReplyPrivateThreadFormset
    from misago.posting.hooks import get_private_thread_reply_context_data_hook
    from misago.threads.models import Thread


    @get_private_thread_reply_context_data_hook.append_filter
    def set_show_first_post_warning_in_context(
        action,
        request: HttpRequest,
        thread: Thread,
        formset: ReplyPrivateThreadFormset,
    ) -> dict:
        context = action(request, thread, formset)
        context["show_first_post_warning"] = not request.user.posts
        return context
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetPrivateThreadReplyContextDataHookAction,
        request: HttpRequest,
        thread: Thread,
        formset: "ReplyPrivateThreadFormset",
    ) -> dict:
        return super().__call__(action, request, thread, formset)


get_private_thread_reply_context_data_hook = GetPrivateThreadReplyContextDataHook(
    cache=False
)
