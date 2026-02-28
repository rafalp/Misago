from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ...users.models import User


class UnwatchThreadHookAction(Protocol):
    """
    Misago function for deleting `WatchedThread` instances
    associated with a user and a thread.

    # Arguments

    ## `thread: Thread`

    The thread to unwatch.

    ## `user: User`

    The user who is unwatching the thread.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if any `WatchedThread` instances were deleted, and `False` if not.
    """

    def __call__(
        self,
        thread: Thread,
        user: "User",
        request: HttpRequest | None = None,
    ) -> bool: ...


class UnwatchThreadHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: UnwatchThreadHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `thread: Thread`

    The thread to unwatch.

    ## `user: User`

    The user who is unwatching the thread.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if any `WatchedThread` instances were deleted, and `False` if not.
    """

    def __call__(
        self,
        action: UnwatchThreadHookAction,
        thread: Thread,
        user: "User",
        request: HttpRequest | None = None,
    ) -> bool: ...


class UnwatchThreadHook(
    FilterHook[
        UnwatchThreadHookAction,
        UnwatchThreadHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    unwatch a thread for a user.”

    # Example

    Record in the database when a user unwatches a thread:

    ```python
    from django.http import HttpRequest
    from misago.notifications.hooks import unwatch_thread_hook
    from misago.threads.models import Thread
    from misago.users.models import User
    from myplugin.models import UnwatchedThread


    @unwatch_thread_hook.append_filter
    def record_unwatched_thread(
        action,
        thread: Thread,
        user: User,
        request: HttpRequest | None = None,
    ) -> bool:
        deleted = action(thread, user, request)

        if deleted:
            UnwatchedThread.objects.create(thread=thread, user=user)

        return deleted
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: UnwatchThreadHookAction,
        thread: Thread,
        user: "User",
        request: HttpRequest | None = None,
    ) -> bool:
        return super().__call__(
            action,
            thread,
            user,
            request,
        )


unwatch_thread_hook = UnwatchThreadHook()
