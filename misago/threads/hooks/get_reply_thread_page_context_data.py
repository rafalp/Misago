from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Thread

if TYPE_CHECKING:
    from ...posting.formsets import ReplyThreadFormset


class GetReplyThreadPageContextDataHookAction(Protocol):
    """
    A standard Misago function used to get the template context data
    for the reply to thread page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    The `Thread` instance.

    ## `formset: ReplyThreadFormset`

    The `ReplyThreadFormset` instance.

    # Return value

    A Python `dict` with context data to use to `render`
    the reply to thread page.
    """

    def __call__(
        self,
        request: HttpRequest,
        thread: Thread,
        formset: "ReplyThreadFormset",
    ) -> dict: ...


class GetReplyThreadPageContextDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetReplyThreadPageContextDataHookAction`

    A standard Misago function used to get the template context data
    for the reply to thread page.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    The `Thread` instance.

    ## `formset: ReplyThreadFormset`

    The `ReplyThreadFormset` instance.

    # Return value

    A Python `dict` with context data to use to `render`
    the reply to thread page.
    """

    def __call__(
        self,
        action: GetReplyThreadPageContextDataHookAction,
        request: HttpRequest,
        thread: Thread,
        formset: "ReplyThreadFormset",
    ) -> dict: ...


class GetReplyThreadPageContextDataHook(
    FilterHook[
        GetReplyThreadPageContextDataHookAction,
        GetReplyThreadPageContextDataHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get the template
    context data for the reply to thread page.

    # Example

    The code below implements a custom filter function that adds extra values to
    the template context data:

    ```python
    from django.http import HttpRequest
    from misago.posting.formsets import ReplyThreadFormset
    from misago.threads.hooks import get_reply_thread_page_context_data_hook
    from misago.threads.models import Thread


    @get_reply_thread_page_context_data_hook.append_filter
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
        action: GetReplyThreadPageContextDataHookAction,
        request: HttpRequest,
        thread: Thread,
        formset: "ReplyThreadFormset",
    ) -> dict:
        return super().__call__(action, request, thread, formset)


get_reply_thread_page_context_data_hook = GetReplyThreadPageContextDataHook(cache=False)
