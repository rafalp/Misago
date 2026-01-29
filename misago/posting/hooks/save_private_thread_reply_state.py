from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..state.reply import PrivateThreadReplyState


class SavePrivateThreadReplyStateHookAction(Protocol):
    """
    A standard function that Misago uses to save
    a new private thread reply to the database.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `state: PrivateThreadReplyState`

    The `PrivateThreadReplyState` object that stores all data to save to the database.
    """

    def __call__(
        self,
        request: HttpRequest,
        state: "PrivateThreadReplyState",
    ): ...


class SavePrivateThreadReplyStateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: SavePrivateThreadReplyStateHookAction`

    The next function registered in this hook, either a custom function or
    Misago's default.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `state: PrivateThreadReplyState`

    The `PrivateThreadReplyState` object that stores all data to save to the database.
    """

    def __call__(
        self,
        action: SavePrivateThreadReplyStateHookAction,
        request: HttpRequest,
        state: "PrivateThreadReplyState",
    ): ...


class SavePrivateThreadReplyStateHook(
    FilterHook[
        SavePrivateThreadReplyStateHookAction, SavePrivateThreadReplyStateHookFilter
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
    from misago.posting.hooks import save_private_thread_reply_state_hook
    from misago.posting.state import PrivateThreadReplyState


    @save_private_thread_reply_state_hook.append_filter
    def save_poster_ip_on_private_thread_reply(
        action, request: HttpRequest, state: PrivateThreadReplyState
    ):
        state.post.plugin_data["poster_ip"] = request.user_ip

        action(request, state)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: SavePrivateThreadReplyStateHookAction,
        request: HttpRequest,
        state: "PrivateThreadReplyState",
    ):
        return super().__call__(action, request, state)


save_private_thread_reply_state_hook = SavePrivateThreadReplyStateHook(cache=False)
