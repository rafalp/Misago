from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Post, Thread

if TYPE_CHECKING:
    from ..state.reply import ReplyThreadState


class GetReplyThreadStateHookAction(Protocol):
    """
    A standard function that Misago uses to create a new `ReplyThreadState`
    instance for replying to a thread.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    The `Thread` instance.

    ## `post: Post | None`

    The `Post` instance to append posted contents to, or `None`.

    # Return value

    A `ReplyThreadState` instance to use to create a reply in a thread
    in the database.
    """

    def __call__(
        self,
        request: HttpRequest,
        thread: Thread,
        post: Post | None = None,
    ) -> "ReplyThreadState": ...


class GetReplyThreadStateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetReplyThreadStateHookAction`

    A standard function that Misago uses to create a new `ReplyThreadState`
    instance for replying to a thread.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    The `Thread` instance.

    ## `post: Post | None`

    The `Post` instance to append posted contents to, or `None`.

    # Return value

    A `ReplyThreadState` instance to use to create a reply in a thread
    in the database.
    """

    def __call__(
        self,
        action: GetReplyThreadStateHookAction,
        request: HttpRequest,
        thread: Thread,
        post: Post | None = None,
    ) -> "ReplyThreadState": ...


class GetReplyThreadStateHook(
    FilterHook[GetReplyThreadStateHookAction, GetReplyThreadStateHookFilter]
):
    """
    This hook wraps the standard function Misago uses to create a new
    `ReplyThreadState` instance for replying to a thread.

    # Example

    The code below implements a custom filter function that stores the user's IP
    in the state.

    ```python
    from django.http import HttpRequest
    from misago.posting.hooks import get_reply_thread_state_hook
    from misago.posting.state import ReplyThreadState
    from misago.threads.models import Post, Thread


    @get_reply_thread_state_hook.append_filter
    def set_poster_ip_on_reply_thread_state(
        action, request: HttpRequest, thread: Thread, post: Post | None = None
    ) -> ReplyThreadState:
        state = action(request, thread)
        state.plugin_state["user_id"] = request.user_ip
        return state
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetReplyThreadStateHookAction,
        request: HttpRequest,
        thread: Thread,
        post: Post | None = None,
    ) -> "ReplyThreadState":
        return super().__call__(action, request, thread, post)


get_reply_thread_state_hook = GetReplyThreadStateHook()
