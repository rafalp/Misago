from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..models import ThreadUpdate


class HideThreadUpdateHookAction(Protocol):
    """
    Misago function used to hide a `ThreadUpdate` object.

    # Arguments

    ## `thread_event: ThreadUpdate`

    A `ThreadUpdate` instance to hide.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.

    # Return value

    `True` if the thread update was hidden, `False` otherwise.
    """

    def __call__(
        self,
        thread_event: "ThreadUpdate",
        request: HttpRequest | None = None,
    ) -> bool: ...


class HideThreadUpdateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: HideThreadUpdateHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `thread_event: ThreadUpdate`

    A `ThreadUpdate` instance to hide.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.

    # Return value

    `True` if the thread update was hidden, `False` otherwise.
    """

    def __call__(
        self,
        action: HideThreadUpdateHookAction,
        thread_event: "ThreadUpdate",
        request: HttpRequest | None = None,
    ) -> bool: ...


class HideThreadUpdateHook(
    FilterHook[
        HideThreadUpdateHookAction,
        HideThreadUpdateHookFilter,
    ]
):
    """
    This hook wraps a standard Misago function used to hide a `ThreadUpdate` object.

    # Example

    The code below implements a custom filter function that stores the client's
    IP address when a thread update is hidden:

    ```python
    from django.http import HttpRequest
    from misago.threads.hooks import hide_thread_event_hook
    from misago.threads.models import ThreadUpdate


    @hide_thread_event_hook.append_filter
    def save_client_ip_on_thread_event_hide(
        action,
        thread_event: ThreadUpdate,
        request: HttpRequest | None = None,
    ) -> bool:
        if not request:
            return action(thread_event)

        thread_event.plugin_data["last_ip"] = request.client_ip

        return action(thread_event, request)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: HideThreadUpdateHookAction,
        thread_event: "ThreadUpdate",
        request: HttpRequest | None = None,
    ) -> "ThreadUpdate":
        return super().__call__(action, thread_event, request)


hide_thread_event_hook = HideThreadUpdateHook()
