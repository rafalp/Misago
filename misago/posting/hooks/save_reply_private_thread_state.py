from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..state.reply import ReplyPrivateThreadState


class SaveReplyPrivateThreadStateHookAction(Protocol):
    """
    A standard function that Misago uses to save
    a new private thread reply to the database.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `state: ReplyPrivateThreadState`

    The `ReplyPrivateThreadState` object that stores all data to save to the database.
    """

    def __call__(
        self,
        request: HttpRequest,
        state: "ReplyPrivateThreadState",
    ): ...


class SaveReplyPrivateThreadStateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: SaveReplyPrivateThreadStateHookAction`

    A standard function that Misago uses to save
    a new private thread reply to the database.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `state: ReplyPrivateThreadState`

    The `ReplyPrivateThreadState` object that stores all data to save to the database.
    """

    def __call__(
        self,
        action: SaveReplyPrivateThreadStateHookAction,
        request: HttpRequest,
        state: "ReplyPrivateThreadState",
    ): ...


class SaveReplyPrivateThreadStateHook(
    FilterHook[
        SaveReplyPrivateThreadStateHookAction, SaveReplyPrivateThreadStateHookFilter
    ]
):
    """
    This hook wraps the standard function that Misago uses to save
    a new private thread reply to the database.

    # Example

    The code below implements a custom filter function that stores the user's IP
    on the saved post.

    ```python
    from django.http import HttpRequest
    from misago.posting.hooks import save_reply_private_thread_state_hook
    from misago.posting.state import ReplyPrivateThreadState


    @save_reply_private_thread_state_hook.append_filter
    def save_poster_ip_on_private_thread_reply(
        action, request: HttpRequest, state: ReplyPrivateThreadState
    ):
        state.post.plugin_data["poster_ip"] = request.user_ip

        action(request, state)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: SaveReplyPrivateThreadStateHookAction,
        request: HttpRequest,
        state: "ReplyPrivateThreadState",
    ):
        return super().__call__(action, request, state)


save_reply_private_thread_state_hook = SaveReplyPrivateThreadStateHook(cache=False)
