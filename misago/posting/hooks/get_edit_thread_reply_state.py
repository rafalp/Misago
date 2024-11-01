from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Post

if TYPE_CHECKING:
    from ..state.edit import EditThreadReplyState


class GetEditThreadReplyStateHookAction(Protocol):
    """
    A standard function that Misago uses to create a new `EditThreadReplyState`
    instance for editing a thread reply.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    # Return value

    A `EditThreadReplyState` instance to use to edit a reply in a thread
    in the database.
    """

    def __call__(
        self,
        request: HttpRequest,
        post: Post,
    ) -> "EditThreadReplyState": ...


class GetEditThreadReplyStateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetEditThreadReplyStateHookAction`

    A standard function that Misago uses to create a new `EditThreadReplyState`
    instance for editing a thread reply.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    # Return value

    A `EditThreadReplyState` instance to use to edit a reply in a thread
    in the database.
    """

    def __call__(
        self,
        action: GetEditThreadReplyStateHookAction,
        request: HttpRequest,
        post: Post,
    ) -> "EditThreadReplyState": ...


class GetEditThreadReplyStateHook(
    FilterHook[GetEditThreadReplyStateHookAction, GetEditThreadReplyStateHookFilter]
):
    """
    This hook wraps the standard function Misago uses to create a new
    `EditThreadReplyState` instance for editing a thread reply.

    # Example

    The code below implements a custom filter function that stores the user's IP
    in the state.

    ```python
    from django.http import HttpRequest
    from misago.posting.hooks import get_edit_thread_reply_state_hook
    from misago.posting.state import EditThreadReplyState
    from misago.threads.models import Post


    @get_edit_thread_reply_state_hook.append_filter
    def set_poster_ip_on_edit_thread_reply_state(
        action, request: HttpRequest, post: Post
    ) -> EditThreadReplyState:
        state = action(request, post)
        state.plugin_state["user_id"] = request.user_ip
        return state
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetEditThreadReplyStateHookAction,
        request: HttpRequest,
        post: Post,
    ) -> "EditThreadReplyState":
        return super().__call__(action, request, post)


get_edit_thread_reply_state_hook = GetEditThreadReplyStateHook()
