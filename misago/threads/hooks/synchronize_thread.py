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

    Defaults to True.

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

    Defaults to True.

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

    Thread synchronization updates a thread’s reply count, the IDs and timestamps
    of the first and last posts, the attributes of the first and last posters,
    and status flags such as has_unapproved_posts.

    # Example

    Record the IP address used to change the thread owner:

    ```python
    from django.http import HttpRequest
    from misago.privatethreadmembers.hooks import synchronize_thread_hook
    from misago.threads.models import Thread
    from misago.threadupdates.models import ThreadUpdate
    from misago.users.models import User


    @synchronize_thread_hook.append_filter
    def record_private_thread_owner_change_actor_ip(
        action,
        actor: User | str | None,
        thread: Thread,
        new_owner: User,
        request: HttpRequest | None = None,
    ) -> ThreadUpdate:
        thread_update = action(actor, thread, new_owner, request)

        thread_update.plugin_data["user_ip"] = request.user_ip
        thread_update.save(update_fields=["plugin_data"])

        return thread_update
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
