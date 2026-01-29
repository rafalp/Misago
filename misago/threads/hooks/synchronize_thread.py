from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Thread


class SynchronizeThreadHookAction(Protocol):
    """
    Misago function for synchronizing a thread.

    # Arguments

    ## `thread: Thread`

    The thread to synchronize.

    ## `data: dict`

    A `dict` of new attributes to set on the thread.

    ## `commit: bool`

    Whether the updated thread instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.
    """

    def __call__(
        self,
        thread: Thread,
        data: dict,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> None: ...


class SynchronizeThreadHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: SynchronizeThreadHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `thread: Thread`

    The thread to synchronize.

    ## `data: dict`

    A `dict` of new attributes to set on the thread.

    ## `commit: bool`

    Whether the updated thread instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.
    """

    def __call__(
        self,
        action: SynchronizeThreadHookAction,
        thread: Thread,
        data: dict,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> None: ...


class SynchronizeThreadHook(
    FilterHook[
        SynchronizeThreadHookAction,
        SynchronizeThreadHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    synchronize threads.

    Thread synchronization updates a thread's reply count, the IDs and timestamps
    of the first and last posts, the attributes of the first and last posters,
    and status flags such as `has_unapproved_posts`.

    # Example

    Record the last user who synchronized the thread:

    ```python
    from django.http import HttpRequest
    from misago.threads.hooks import synchronize_thread_hook
    from misago.threads.models import Thread


    @synchronize_thread_hook.append_filter
    def record_user_who_synced_thread(
        action,
        thread: Thread,
        data: dict,
        commit: bool = True,
        request: HttpRequest | None = None,
    ):
        if "plugin_data" not in data:
            data["plugin_data"] = thread.plugin_data

        if request:
            data["plugin_data"]["last_synchronized"] = {
                "user_id": request.user.id,
                "user_ip": request.user_ip,
            }
        else:
            data["plugin_data"]["last_synchronized"] = None

        action(thread, data, commit, request)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: SynchronizeThreadHookAction,
        thread: Thread,
        data: dict,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> None:
        return super().__call__(
            action,
            thread,
            data,
            commit,
            request,
        )


synchronize_thread_hook = SynchronizeThreadHook()
