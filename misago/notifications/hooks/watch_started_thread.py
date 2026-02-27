from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Thread
from ..models import WatchedThread

if TYPE_CHECKING:
    from ...users.models import User


class WatchStartedThreadHookAction(Protocol):
    """
    Misago function for creating a new `WatchedThread` instance for a started thread.

    # Arguments

    ## `thread: Thread`

    The thread to watch.

    ## `user: User`

    The user who started to the thread.

    ## `commit: bool`

    Whether the new `WatchedThread` instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    New `WatchedThread` instance, or `None` if the user has disabled the option
    to watch started threads.
    """

    def __call__(
        self,
        thread: Thread,
        user: "User",
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> WatchedThread | None: ...


class WatchStartedThreadHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: WatchStartedThreadHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `thread: Thread`

    The thread to watch.

    ## `user: User`

    The user who started to the thread.

    ## `commit: bool`

    Whether the new `WatchedThread` instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    New `WatchedThread` instance, or `None` if the user has disabled the option
    to watch started threads.
    """

    def __call__(
        self,
        action: WatchStartedThreadHookAction,
        thread: Thread,
        user: "User",
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> WatchedThread | None: ...


class WatchStartedThreadHook(
    FilterHook[
        WatchStartedThreadHookAction,
        WatchStartedThreadHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    create a watched thread object when user starts a new thread.

    # Example

    Record the IP address used to watch the thread:

    ```python
    from django.http import HttpRequest
    from misago.notifications.hooks import watch_started_thread_hook
    from misago.notifications.models import WatchedThread
    from misago.threads.models import Thread
    from misago.users.models import User


    @watch_started_thread_hook.append_filter
    def record_watched_thread_user_ip(
        action,
        thread: Thread,
        user: User,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> WatchedThread | None:
        watched_thread = action(thread, user, send_emails, False, request)
        if watched_thread:
            watched_thread.plugin_data["user_id"] = request.user_ip
            if commit:
                watched_thread.save()

        return watched_thread
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: WatchStartedThreadHookAction,
        thread: Thread,
        user: "User",
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> WatchedThread | None:
        return super().__call__(
            action,
            thread,
            user,
            commit,
            request,
        )


watch_started_thread_hook = WatchStartedThreadHook()
