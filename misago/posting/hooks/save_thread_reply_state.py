from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..state.reply import ThreadReplyState


class SaveThreadReplyStateHookAction(Protocol):
    """
    A standard function that Misago uses to save
    a new thread reply to the database.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `state: ThreadReplyState`

    The `ThreadReplyState` object that stores all data to save to the database.
    """

    def __call__(
        self,
        request: HttpRequest,
        state: "ThreadReplyState",
    ): ...


class SaveThreadReplyStateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: SaveThreadReplyStateHookAction`

    The next function registered in this hook, either a custom function or
    Misago's default.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `state: ThreadReplyState`

    The `ThreadReplyState` object that stores all data to save to the database.
    """

    def __call__(
        self,
        action: SaveThreadReplyStateHookAction,
        request: HttpRequest,
        state: "ThreadReplyState",
    ): ...


class SaveThreadReplyStateHook(
    FilterHook[SaveThreadReplyStateHookAction, SaveThreadReplyStateHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to save
    a new thread reply to the database.

    # Example

    The code below implements a custom filter function that stores the user's IP
    on the saved post.

    ```python
    from django.http import HttpRequest
    from misago.posting.hooks import save_thread_reply_state_hook
    from misago.posting.state import ThreadReplyState


    @save_thread_reply_state_hook.append_filter
    def save_poster_ip_on_thread_reply(
        action, request: HttpRequest, state: ThreadReplyState
    ):
        state.post.plugin_data["poster_ip"] = request.user_ip

        action(request, state)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: SaveThreadReplyStateHookAction,
        request: HttpRequest,
        state: "ThreadReplyState",
    ):
        return super().__call__(action, request, state)


save_thread_reply_state_hook = SaveThreadReplyStateHook(cache=False)
