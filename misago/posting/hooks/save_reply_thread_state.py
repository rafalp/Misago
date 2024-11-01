from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..state.reply import ReplyThreadState


class SaveReplyThreadStateHookAction(Protocol):
    """
    A standard function that Misago uses to save
    a new thread reply to the database.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `state: ReplyThreadState`

    The `ReplyThreadState` object that stores all data to save to the database.
    """

    def __call__(
        self,
        request: HttpRequest,
        state: "ReplyThreadState",
    ): ...


class SaveReplyThreadStateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: SaveReplyThreadStateHookAction`

    A standard function that Misago uses to save
    a new thread reply to the database.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `state: ReplyThreadState`

    The `ReplyThreadState` object that stores all data to save to the database.
    """

    def __call__(
        self,
        action: SaveReplyThreadStateHookAction,
        request: HttpRequest,
        state: "ReplyThreadState",
    ): ...


class SaveReplyThreadStateHook(
    FilterHook[SaveReplyThreadStateHookAction, SaveReplyThreadStateHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to save
    a new thread reply to the database.

    # Example

    The code below implements a custom filter function that stores the user's IP
    on the saved post.

    ```python
    from django.http import HttpRequest
    from misago.posting.hooks import save_reply_thread_state_hook
    from misago.posting.state import ReplyThreadState


    @save_reply_thread_state_hook.append_filter
    def save_poster_ip_on_thread_reply(
        action, request: HttpRequest, state: ReplyThreadState
    ):
        state.post.plugin_data["poster_ip"] = request.user_ip

        action(request, state)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: SaveReplyThreadStateHookAction,
        request: HttpRequest,
        state: "ReplyThreadState",
    ):
        return super().__call__(action, request, state)


save_reply_thread_state_hook = SaveReplyThreadStateHook(cache=False)
