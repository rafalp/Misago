from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Post, Thread

if TYPE_CHECKING:
    from ..state.reply import ThreadReplyState


class GetThreadReplyStateHookAction(Protocol):
    """
    Misago function used to create a new `ThreadReplyState` instance
    for the thread reply view.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    The `Thread` instance.

    ## `post: Post | None`

    The `Post` instance to append posted contents to, or `None`.

    # Return value

    A `ThreadReplyState` instance to use to create a reply in a thread
    in the database.
    """

    def __call__(
        self,
        request: HttpRequest,
        thread: Thread,
        post: Post | None = None,
    ) -> "ThreadReplyState": ...


class GetThreadReplyStateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadReplyStateHookAction`

    The next function registered in this hook, either a custom function or
    Misago's default.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    The `Thread` instance.

    ## `post: Post | None`

    The `Post` instance to append posted contents to, or `None`.

    # Return value

    A `ThreadReplyState` instance to use to create a reply in a thread
    in the database.
    """

    def __call__(
        self,
        action: GetThreadReplyStateHookAction,
        request: HttpRequest,
        thread: Thread,
        post: Post | None = None,
    ) -> "ThreadReplyState": ...


class GetThreadReplyStateHook(
    FilterHook[GetThreadReplyStateHookAction, GetThreadReplyStateHookFilter]
):
    """
    This hook wraps the standard function Misago uses to create a new
    `ThreadReplyState` instance for the thread reply view.

    # Example

    The code below implements a custom filter function that stores the user's IP
    in the state.

    ```python
    from django.http import HttpRequest
    from misago.posting.hooks import get_thread_reply_state_hook
    from misago.posting.state import ThreadReplyState
    from misago.threads.models import Post, Thread


    @get_thread_reply_state_hook.append_filter
    def set_poster_ip_on_reply_thread_state(
        action,
        request: HttpRequest,
        thread: Thread,
        post: Post | None = None,
    ) -> ThreadReplyState:
        state = action(request, thread)
        state.plugin_state["user_id"] = request.user_ip
        return state
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadReplyStateHookAction,
        request: HttpRequest,
        thread: Thread,
        post: Post | None = None,
    ) -> "ThreadReplyState":
        return super().__call__(action, request, thread, post)


get_thread_reply_state_hook = GetThreadReplyStateHook()
