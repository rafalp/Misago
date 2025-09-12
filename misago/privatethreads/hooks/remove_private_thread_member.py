from typing import TYPE_CHECKING, Protocol, Union

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ...threadupdates.models import ThreadUpdate
    from ...users.models import User


class RemovePrivateThreadMemberAction(Protocol):
    """
    Misago function for removing a member from a private thread.

    # Arguments

    ## `actor: User | str | None`

    The actor performing the action: either a `User` instance, a `str` with a name,
    or `None` if not available.

    ## `thread: Thread`

    The thread from which the member will be removed.

    ## `member: User`

    The user to remove from the thread.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    A `ThreadUpdate` instance.
    """

    def __call__(
        self,
        actor: Union["User", str, None],
        thread: Thread,
        member: "User",
        request: HttpRequest | None = None,
    ) -> "ThreadUpdate": ...


class RemovePrivateThreadMemberFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: RemovePrivateThreadMemberAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `actor: User | str | None`

    The actor performing the action: either a `User` instance, a `str` with a name,
    or `None` if not available.

    ## `thread: Thread`

    The thread from which the member will be removed.

    ## `member: User`

    The user to remove from the thread.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    A `ThreadUpdate` instance.
    """

    def __call__(
        self,
        action: RemovePrivateThreadMemberAction,
        actor: Union["User", str, None],
        thread: Thread,
        member: "User",
        request: HttpRequest | None = None,
    ) -> "ThreadUpdate": ...


class RemovePrivateThreadMember(
    FilterHook[
        RemovePrivateThreadMemberAction,
        RemovePrivateThreadMemberFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic for
    removing a member from a private thread.

    # Example

    Record the IP address used to remove a member from a thread:

    ```python
    from django.http import HttpRequest
    from misago.privatethreads.hooks import remove_private_thread_member_hook
    from misago.threads.models import Thread
    from misago.threadupdates.models import ThreadUpdate
    from misago.users.models import User


    @remove_private_thread_member_hook.append_filter
    def record_private_thread_remove_member_actor_ip(
        action,
        actor: User | str | None,
        thread: Thread,
        member: User,
        request: HttpRequest | None = None,
    ) -> ThreadUpdate:
        thread_update = action(actor, thread, member, request)

        thread_update.plugin_data["user_ip"] = request.user_ip
        thread_update.save(update_fields=["plugin_data"])

        return thread_update
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: RemovePrivateThreadMemberAction,
        actor: Union["User", str, None],
        thread: Thread,
        member: "User",
        request: HttpRequest | None = None,
    ) -> "ThreadUpdate":
        return super().__call__(
            action,
            actor,
            thread,
            member,
            request,
        )


remove_private_thread_member_hook = RemovePrivateThreadMember()
