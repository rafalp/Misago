from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..state.reply import ReplyPrivateThreadState


class GetReplyPrivateThreadStateHookAction(Protocol):
    """
    A standard function that Misago uses to create a new `ReplyPrivateThreadState`
    instance for replying to a private thread.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    The `Thread` instance.

    # Return value

    A `ReplyPrivateThreadState` instance to use to create a reply in a private thread
    in the database.
    """

    def __call__(
        self,
        request: HttpRequest,
        thread: Thread,
    ) -> "ReplyPrivateThreadState": ...


class GetReplyPrivateThreadStateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetReplyPrivateThreadStateHookAction`

    A standard function that Misago uses to create a new `ReplyPrivateThreadState`
    instance for replying to a private thread.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    The `Thread` instance.

    # Return value

    A `ReplyPrivateThreadState` instance to use to create a reply in a private thread
    in the database.
    """

    def __call__(
        self,
        action: GetReplyPrivateThreadStateHookAction,
        request: HttpRequest,
        thread: Thread,
    ) -> "ReplyPrivateThreadState": ...


class GetReplyPrivateThreadStateHook(
    FilterHook[
        GetReplyPrivateThreadStateHookAction, GetReplyPrivateThreadStateHookFilter
    ]
):
    """
    This hook wraps the standard function Misago uses to create a new
    `ReplyPrivateThreadState` instance for replying to a private thread.

    # Example

    The code below implements a custom filter function that stores the user's IP
    in the state.

    ```python
    from django.http import HttpRequest
    from misago.posting.hooks import get_reply_private_thread_state_hook
    from misago.posting.state import ReplyPrivateThreadState
    from misago.threads.models import Thread


    @get_reply_private_thread_state_hook.append_filter
    def set_poster_ip_on_reply_private_thread_state(
        action, request: HttpRequest, thread: Thread
    ) -> ReplyPrivateThreadState:
        state = action(request, thread)
        state.plugin_state["user_id"] = request.user_ip
        return state
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetReplyPrivateThreadStateHookAction,
        request: HttpRequest,
        thread: Thread,
    ) -> "ReplyPrivateThreadState":
        return super().__call__(action, request, thread)


get_reply_private_thread_state_hook = GetReplyPrivateThreadStateHook()
