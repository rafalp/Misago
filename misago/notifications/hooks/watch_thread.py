from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Thread
from ..models import WatchedThread

if TYPE_CHECKING:
    from ...users.models import User


class WatchThreadHookAction(Protocol):
    """
    Misago function for creating a new `WatchedThread` instance.

    # Arguments

    ## `thread: Thread`

    The thread to watch.

    ## `user: User`

    The user who is watching the thread.

    ## `send_emails: bool`

    Whether e-mail notifications should be enabled.

    Defaults to `True`,

    ## `commit: bool`

    Whether the new `WatchedThread` instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    New `WatchedThread` instance.
    """

    def __call__(
        self,
        thread: Thread,
        user: "User",
        send_emails: bool = True,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> WatchedThread: ...


class WatchThreadHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: WatchThreadHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `thread: Thread`

    The thread to watch.

    ## `user: User`

    The user who is watching the thread.

    ## `send_emails: bool`

    Whether e-mail notifications should be enabled.

    Defaults to `True`,

    ## `commit: bool`

    Whether the new `WatchedThread` instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    New `WatchedThread` instance.
    """

    def __call__(
        self,
        action: WatchThreadHookAction,
        thread: Thread,
        user: "User",
        send_emails: bool = True,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> WatchedThread: ...


class WatchThreadHook(
    FilterHook[
        WatchThreadHookAction,
        WatchThreadHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    create watched thread objects.

    # Example

    Record the IP address used to watch the thread:

    ```python
    from django.http import HttpRequest
    from misago.notifications.hooks import watch_thread_hook
    from misago.notifications.models import WatchedThread
    from misago.threads.models import Thread
    from misago.users.models import User


    @watch_thread_hook.append_filter
    def record_watched_thread_user_ip(
        action,
        thread: Thread,
        user: User,
        send_emails: bool = True,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> WatchedThread:
        watched_thread = action(thread, user, send_emails, False, request)

        watched_thread.plugin_data["user_id"] = request.user_ip

        if commit:
            watched_thread.save()

        return watched_thread
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: WatchThreadHookAction,
        thread: Thread,
        user: "User",
        send_emails: bool = True,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> WatchedThread:
        return super().__call__(
            action,
            thread,
            user,
            send_emails,
            commit,
            request,
        )


watch_thread_hook = WatchThreadHook()
