from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ...users.models import User


class SetPrivateThreadOwnerHookAction(Protocol):
    """
    Misago function for setting the owner of a private thread.

    # Arguments

    ## `thread: Thread`

    The thread whose owner will be set.

    ## `new_owner: User`

    The user to set as the thread's new owner.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    A `bool`: `True` if the new owner was set, or `False` otherwise.
    """

    def __call__(
        self,
        thread: Thread,
        new_owner: "User",
        request: HttpRequest | None = None,
    ) -> "bool": ...


class SetPrivateThreadOwnerHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: SetPrivateThreadOwnerHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `thread: Thread`

    The thread whose owner will be set.

    ## `new_owner: User`

    The user to set as the thread's new owner.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    A `bool`: `True` if the new owner was set, or `False` otherwise.
    """

    def __call__(
        self,
        action: SetPrivateThreadOwnerHookAction,
        thread: Thread,
        new_owner: "User",
        request: HttpRequest | None = None,
    ) -> "bool": ...


class SetPrivateThreadOwnerHook(
    FilterHook[
        SetPrivateThreadOwnerHookAction,
        SetPrivateThreadOwnerHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic for setting
    the owner of a private thread.

    # Example

    Record the user who set the thread owner:

    ```python
    from django.http import HttpRequest
    from misago.privatethreads.hooks import set_private_thread_owner_hook
    from misago.threads.models import Thread
    from misago.users.models import User


    @set_private_thread_owner_hook.append_filter
    def record_private_thread_owner_set_actor(
        action,
        thread: Thread,
        new_owner: User,
        request: HttpRequest | None = None,
    ) -> bool:
        set_owner = action(thread, new_owner, request)

        if set_owner and request:
            thread.plugin_data["set_owner"] = {
                "user_id": request.user.id,
                "user_ip": request.user_ip,
            }
            thread.save(update_fields=["plugin_data"])

        return set_owner
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: SetPrivateThreadOwnerHookAction,
        thread: Thread,
        new_owner: "User",
        request: HttpRequest | None = None,
    ) -> "bool":
        return super().__call__(
            action,
            thread,
            new_owner,
            request,
        )


set_private_thread_owner_hook = SetPrivateThreadOwnerHook()
