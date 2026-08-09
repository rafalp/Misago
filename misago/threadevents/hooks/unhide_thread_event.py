from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..models import ThreadEvent


class UnhideThreadEventHookAction(Protocol):
    """
    Misago function used to unhide a `ThreadEvent` object.

    # Arguments

    ## `thread_event: ThreadEvent`

    A `ThreadEvent` instance to unhide.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.

    # Return value

    `True` if the thread event was unhidden, `False` otherwise.
    """

    def __call__(
        self,
        thread_event: "ThreadEvent",
        request: HttpRequest | None = None,
    ) -> bool: ...


class UnhideThreadEventHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: UnhideThreadEventHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `thread_event: ThreadEvent`

    A `ThreadEvent` instance to unhide.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.

    # Return value

    `True` if the thread event was unhidden, `False` otherwise.
    """

    def __call__(
        self,
        action: UnhideThreadEventHookAction,
        thread_event: "ThreadEvent",
        request: HttpRequest | None = None,
    ) -> bool: ...


class UnhideThreadEventHook(
    FilterHook[
        UnhideThreadEventHookAction,
        UnhideThreadEventHookFilter,
    ]
):
    """
    This hook wraps a standard Misago function used to unhide a `ThreadEvent` object.

    # Example

    The code below implements a custom filter function that stores the client's
    IP address when a thread event is unhidden:

    ```python
    from django.http import HttpRequest
    from misago.threadevents.hooks import unhide_thread_event_hook
    from misago.threadevents.models import ThreadEvent


    @unhide_thread_event_hook.append_filter
    def save_client_ip_on_thread_event_unhide(
        action,
        thread_event: ThreadEvent,
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
        action: UnhideThreadEventHookAction,
        thread_event: "ThreadEvent",
        request: HttpRequest | None = None,
    ) -> "ThreadEvent":
        return super().__call__(action, thread_event, request)


unhide_thread_event_hook = UnhideThreadEventHook()
