from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..models import ThreadUpdate


class DeleteThreadUpdateHookAction(Protocol):
    """
    Misago function used to delete a `ThreadUpdate` object.

    # Arguments

    ## `thread_update: ThreadUpdate`

    A `ThreadUpdate` instance to delete.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.
    """

    def __call__(
        self,
        thread_update: "ThreadUpdate",
        request: HttpRequest | None = None,
    ): ...


class DeleteThreadUpdateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: DeleteThreadUpdateHookAction`

    Misago function used to delete a `ThreadUpdate` object.

    ## `thread_update: ThreadUpdate`

    A `ThreadUpdate` instance to delete.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.
    """

    def __call__(
        self,
        action: DeleteThreadUpdateHookAction,
        thread_update: "ThreadUpdate",
        request: HttpRequest | None = None,
    ): ...


class DeleteThreadUpdateHook(
    FilterHook[
        DeleteThreadUpdateHookAction,
        DeleteThreadUpdateHookFilter,
    ]
):
    """
    This hook wraps a standard Misago function used to delete a `ThreadUpdate` object.

    # Example

    The code below implements a custom filter function that logs the deletion
    of a thread update:

    ```python
    import logging

    from django.http import HttpRequest
    from misago.threads.hooks import delete_thread_update_hook
    from misago.threads.models import ThreadUpdate

    logger = logging.getLogger("misago.moderation")


    @delete_thread_update_hook.append_filter
    def log_thread_update_deletion(
        action,
        thread_update: ThreadUpdate,
        request: HttpRequest | None = None,
    ) -> bool:
        logger.info(
            "Thread update was deleted",
            extra={
                "id": thread_update.id,
                "user": request.user.id if request else "",
                "ip": request.client_ip if request else "",
            },
        )
        return action(thread_update, request)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: DeleteThreadUpdateHookAction,
        thread_update: "ThreadUpdate",
        update_fields: set[str],
        request: HttpRequest | None = None,
    ) -> "ThreadUpdate":
        return super().__call__(action, thread_update, request)


delete_thread_update_hook = DeleteThreadUpdateHook()
