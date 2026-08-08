from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..models import ThreadEvent


class DeleteThreadEventHookAction(Protocol):
    """
    Misago function used to delete a `ThreadEvent` object.

    # Arguments

    ## `thread_event: ThreadEvent`

    A `ThreadEvent` instance to delete.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.
    """

    def __call__(
        self,
        thread_event: "ThreadEvent",
        request: HttpRequest | None = None,
    ): ...


class DeleteThreadEventHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: DeleteThreadEventHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `thread_event: ThreadEvent`

    A `ThreadEvent` instance to delete.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.
    """

    def __call__(
        self,
        action: DeleteThreadEventHookAction,
        thread_event: "ThreadEvent",
        request: HttpRequest | None = None,
    ): ...


class DeleteThreadEventHook(
    FilterHook[
        DeleteThreadEventHookAction,
        DeleteThreadEventHookFilter,
    ]
):
    """
    This hook wraps a standard Misago function used to delete a `ThreadEvent` object.

    # Example

    The code below implements a custom filter function that logs the deletion
    of a thread event:

    ```python
    import logging

    from django.http import HttpRequest
    from misago.threadevents.hooks import delete_thread_event_hook
    from misago.threadevents.models import ThreadEvent

    logger = logging.getLogger("misago.threadevents")


    @delete_thread_event_hook.append_filter
    def log_thread_event_deletion(
        action,
        thread_event: ThreadEvent,
        request: HttpRequest | None = None,
    ) -> bool:
        logger.info(
            "Thread event was deleted",
            extra={
                "id": thread_event.id,
                "user": request.user.id if request else "",
                "ip": request.client_ip if request else "",
            },
        )
        return action(thread_event, request)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: DeleteThreadEventHookAction,
        thread_event: "ThreadEvent",
        update_fields: set[str],
        request: HttpRequest | None = None,
    ) -> "ThreadEvent":
        return super().__call__(action, thread_event, request)


delete_thread_event_hook = DeleteThreadEventHook()
