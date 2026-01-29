from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..formsets import ReplyThreadFormset


class GetThreadReplyContextDataHookAction(Protocol):
    """
    Misago function used to get the template context data
    for the thread reply view.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    The `Thread` instance.

    ## `formset: ReplyThreadFormset`

    The `ReplyThreadFormset` instance.

    # Return value

    A Python `dict` with context data used to `render`
    the thread thread reply view.
    """

    def __call__(
        self,
        request: HttpRequest,
        thread: Thread,
        formset: "ReplyThreadFormset",
    ) -> dict: ...


class GetThreadReplyContextDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadReplyContextDataHookAction`

    The next function registered in this hook, either a custom function or
    Misago's default.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    The `Thread` instance.

    ## `formset: ReplyThreadFormset`

    The `ReplyThreadFormset` instance.

    # Return value

    A Python `dict` with context data used to `render`
    the thread thread reply view.
    """

    def __call__(
        self,
        action: GetThreadReplyContextDataHookAction,
        request: HttpRequest,
        thread: Thread,
        formset: "ReplyThreadFormset",
    ) -> dict: ...


class GetThreadReplyContextDataHook(
    FilterHook[
        GetThreadReplyContextDataHookAction,
        GetThreadReplyContextDataHookFilter,
    ]
):
    """
    This hook wraps the function Misago uses to get the template context data
    for the thread reply view.

    # Example

    The code below implements a custom filter function that adds extra values to
    the template context data:

    ```python
    from django.http import HttpRequest
    from misago.posting.formsets import ReplyThreadFormset
    from misago.threads.posting import get_thread_reply_context_data_hook
    from misago.threads.models import Thread


    @get_thread_reply_context_data_hook.append_filter
    def set_show_first_post_warning_in_context(
        action,
        request: HttpRequest,
        thread: Thread,
        formset: ReplyThreadFormset,
    ) -> dict:
        context = action(request, thread, formset)
        context["show_first_post_warning"] = not request.user.posts
        return context
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadReplyContextDataHookAction,
        request: HttpRequest,
        thread: Thread,
        formset: "ReplyThreadFormset",
    ) -> dict:
        return super().__call__(action, request, thread, formset)


get_thread_reply_context_data_hook = GetThreadReplyContextDataHook(cache=False)
