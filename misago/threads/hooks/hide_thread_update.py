from typing import TYPE_CHECKING, Protocol

from django.db.models import Model
from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..models import ThreadUpdate


class HideThreadUpdateHookAction(Protocol):
    """
    A standard Misago function used to hide a `ThreadUpdate` object.

    # Arguments

    ## `thread_update: ThreadUpdate`

    A `ThreadUpdate` instance to hide.

    ## `update_fields: set[str]`

    A `set` of `str` containing the names of fields to pass to the `update(update_fields=...)` option.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.

    # Return value

    `True` if the thread update was hidden, `False` otherwise.
    """

    def __call__(
        self,
        thread_update: "ThreadUpdate",
        update_fields: set[str],
        request: HttpRequest | None = None,
    ) -> bool: ...


class HideThreadUpdateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: HideThreadUpdateHookAction`

    A standard Misago function used to hide a `ThreadUpdate` object.

    ## `thread_update: ThreadUpdate`

    A `ThreadUpdate` instance to hide.

    ## `update_fields: set[str]`

    A `set` of `str` containing the names of fields to pass to the `update(update_fields=...)` option.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.

    # Return value

    `True` if the thread update was hidden, `False` otherwise.
    """

    def __call__(
        self,
        action: HideThreadUpdateHookAction,
        thread_update: "ThreadUpdate",
        update_fields: set[str],
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
    from misago.threads.hooks import hide_thread_update_hook
    from misago.threads.models import ThreadUpdate


    @hide_thread_update_hook.append_filter
    def save_client_ip_on_thread_update(
        action,
        thread_update: ThreadUpdate,
        update_fields: set[str],
        request: HttpRequest | None = None,
    ) -> bool:
        if not request:
            return action(thread_update, update_fields, request)

        thread_update.plugin_data["last_ip"] = request.client_ip
        update_fields.add("plugin_data")

        return action(thread_update, update_fields, request)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: HideThreadUpdateHookAction,
        thread_update: "ThreadUpdate",
        update_fields: set[str],
        request: HttpRequest | None = None,
    ) -> "ThreadUpdate":
        return super().__call__(
            action,
            thread_update,
            update_fields,
            request,
        )


hide_thread_update_hook = HideThreadUpdateHook()
