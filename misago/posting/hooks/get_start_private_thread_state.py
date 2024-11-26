from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...categories.models import Category
from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..state.start import StartPrivateThreadState


class GetStartPrivateThreadStateHookAction(Protocol):
    """
    A standard function that Misago uses to create a new `StartPrivateThreadState`
    instance for starting a new private thread.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    The `Category` instance.

    # Return value

    A `StartPrivateThreadState` instance to use to create a new private thread
    in the database.
    """

    def __call__(
        self,
        request: HttpRequest,
        category: Category,
    ) -> "StartPrivateThreadState": ...


class GetStartPrivateThreadStateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetStartPrivateThreadStateHookAction`

    A standard function that Misago uses to create a new `StartPrivateThreadState`
    instance for starting a new private thread.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    The `Category` instance.

    # Return value

    A `StartPrivateThreadState` instance to use to create a new private thread
    in the database.
    """

    def __call__(
        self,
        action: GetStartPrivateThreadStateHookAction,
        request: HttpRequest,
        category: Category,
    ) -> "StartPrivateThreadState": ...


class GetStartPrivateThreadStateHook(
    FilterHook[
        GetStartPrivateThreadStateHookAction, GetStartPrivateThreadStateHookFilter
    ]
):
    """
    This hook wraps the standard function Misago uses to create a new
    `StartPrivateThreadState` instance for starting a new private thread.

    # Example

    The code below implements a custom filter function that stores the user's IP
    in the state.

    ```python
    from django.http import HttpRequest
    from misago.categories.models import Category
    from misago.posting.hooks import get_start_private_thread_state_hook
    from misago.posting.state import StartPrivateThreadState


    @get_start_private_thread_state_hook.append_filter
    def set_poster_ip_on_start_private_thread_state(
        action, request: HttpRequest, category: Category
    ) -> StartPrivateThreadState:
        state = action(request, category)
        state.plugin_state["user_id"] = request.user_ip
        return state
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetStartPrivateThreadStateHookAction,
        request: HttpRequest,
        category: Category,
    ) -> "StartPrivateThreadState":
        return super().__call__(action, request, category)


get_start_private_thread_state_hook = GetStartPrivateThreadStateHook()
