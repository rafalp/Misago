from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..state.edit import EditPrivateThreadReplyState


class SaveEditPrivateThreadReplyStateHookAction(Protocol):
    """
    A standard function that Misago uses to save
    edited private thread reply to the database.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `state: EditPrivateThreadReplyState`

    The `EditPrivateThreadReplyState` object that stores all data to save to the database.
    """

    def __call__(
        self,
        request: HttpRequest,
        state: "EditPrivateThreadReplyState",
    ): ...


class SaveEditPrivateThreadReplyStateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: SaveEditPrivateThreadReplyStateHookAction`

    A standard function that Misago uses to save
    edited private thread reply to the database.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `state: EditPrivateThreadReplyState`

    The `EditPrivateThreadReplyState` object that stores all data to save to the database.
    """

    def __call__(
        self,
        action: SaveEditPrivateThreadReplyStateHookAction,
        request: HttpRequest,
        state: "EditPrivateThreadReplyState",
    ): ...


class SaveEditPrivateThreadReplyStateHook(
    FilterHook[
        SaveEditPrivateThreadReplyStateHookAction,
        SaveEditPrivateThreadReplyStateHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to save
    edited private thread reply to the database.

    # Example

    The code below implements a custom filter function that stores the user's IP
    on the edited post.

    ```python
    from django.http import HttpRequest
    from misago.posting.hooks import save_edit_private_thread_reply_state_hook
    from misago.posting.state import EditPrivateThreadReplyState


    @save_edit_private_thread_reply_state_hook.append_filter
    def save_poster_ip_on_private_thread_reply(
        action, request: HttpRequest, state: EditPrivateThreadReplyState
    ):
        state.post.plugin_data["editor_ip"] = request.user_ip

        action(request, state)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: SaveEditPrivateThreadReplyStateHookAction,
        request: HttpRequest,
        state: "EditPrivateThreadReplyState",
    ):
        return super().__call__(action, request, state)


save_edit_private_thread_reply_state_hook = SaveEditPrivateThreadReplyStateHook(
    cache=False
)
