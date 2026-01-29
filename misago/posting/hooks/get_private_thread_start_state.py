from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...categories.models import Category
from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..state.start import PrivateThreadStartState


class GetPrivateThreadStartStateHookAction(Protocol):
    """
    A standard function that Misago uses to create a new `PrivateThreadStartState`
    instance for starting a new private thread.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    The `Category` instance.

    # Return value

    A `PrivateThreadStartState` instance to use to create a new private thread
    in the database.
    """

    def __call__(
        self,
        request: HttpRequest,
        category: Category,
    ) -> "PrivateThreadStartState": ...


class GetPrivateThreadStartStateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetPrivateThreadStartStateHookAction`

    The next function registered in this hook, either a custom function or
    Misago's default.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    The `Category` instance.

    # Return value

    A `PrivateThreadStartState` instance to use to create a new private thread
    in the database.
    """

    def __call__(
        self,
        action: GetPrivateThreadStartStateHookAction,
        request: HttpRequest,
        category: Category,
    ) -> "PrivateThreadStartState": ...


class GetPrivateThreadStartStateHook(
    FilterHook[
        GetPrivateThreadStartStateHookAction, GetPrivateThreadStartStateHookFilter
    ]
):
    """
    This hook wraps the standard function Misago uses to create a new
    `PrivateThreadStartState` instance for starting a new private thread.

    # Example

    The code below implements a custom filter function that stores the user's IP
    in the state.

    ```python
    from django.http import HttpRequest
    from misago.categories.models import Category
    from misago.posting.hooks import get_private_thread_start_state_hook
    from misago.posting.state import PrivateThreadStartState


    @get_private_thread_start_state_hook.append_filter
    def set_poster_ip_on_start_private_thread_state(
        action, request: HttpRequest, category: Category
    ) -> PrivateThreadStartState:
        state = action(request, category)
        state.plugin_state["user_id"] = request.user_ip
        return state
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetPrivateThreadStartStateHookAction,
        request: HttpRequest,
        category: Category,
    ) -> "PrivateThreadStartState":
        return super().__call__(action, request, category)


get_private_thread_start_state_hook = GetPrivateThreadStartStateHook()
