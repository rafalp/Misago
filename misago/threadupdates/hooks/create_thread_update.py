from typing import TYPE_CHECKING, Protocol, Union

from django.db.models import Model
from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ...threads.models import Thread
    from ...users.models import User
    from ..models import ThreadUpdate


class CreateThreadUpdateHookAction(Protocol):
    """
    Misago function used to create a `ThreadUpdate` object.

    # Arguments

    ## `thread: Thread`

    A `Thread` instance.

    ## `action_name: str`

    A `str` with the name of the action that updated the thread.

    ## `actor: Union["User", None, str] = None`

    The actor who performed the action: a `User` instance, a `str` with a name,
    or `None` if not available.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.

    ## `context: str | None = None`

    A `str` with context, e.g., a previous thread title or the name of
    `context_object`. `None` if not available or not used for this `action_name`.

    ## `context_object: Model | None = None`

    A `Model` instance that this update object should store a generic relation to.

    ## `is_hidden: bool = False`

    Controls whether the newly created update should be hidden. Hidden updates
    are only visible to moderators but can be made visible to all users.
    Defaults to `False`.

    ## `plugin_data: dict`

    A plugin data `dict` that will be saved on the `ThreadUpdate.plugin_data` attribute.

    # Return value

    A newly created `ThreadUpdate` instance.
    """

    def __call__(
        self,
        thread: "Thread",
        action_name: str,
        actor: Union["User", None, str] = None,
        *,
        request: HttpRequest | None = None,
        context: str | None = None,
        context_object: Model | None = None,
        is_hidden: bool = False,
        plugin_data: dict,
    ) -> "ThreadUpdate": ...


class CreateThreadUpdateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CreateThreadUpdateHookAction`

    Misago function used to create a `ThreadUpdate` object.

    ## `thread: Thread`

    A `Thread` instance.

    ## `action_name: str`

    A `str` with the name of the action that updated the thread.

    ## `actor: Union["User", None, str] = None`

    A `str` with context, e.g., a previous thread title or the name of
    `context_object`. `None` if not available or not used for this `action_name`.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.

    ## `context: str | None = None`

    A `str` with context, e.g., a previous thread title or the name of
    `context_object`. `None` if not available or not used for this `action_name`.

    ## `context_object: Model | None = None`

    A `Model` instance that this update object should store a generic relation to.

    ## `is_hidden: bool = False`

    Controls whether the newly created update should be hidden. Hidden updates
    are only visible to moderators but can be made visible to all users.
    Defaults to `False`.

    ## `plugin_data: dict`

    A plugin data `dict` that will be saved on the `ThreadUpdate.plugin_data` attribute.

    # Return value

    A newly created `ThreadUpdate` instance.
    """

    def __call__(
        self,
        action: CreateThreadUpdateHookAction,
        thread: "Thread",
        action_name: str,
        actor: Union["User", None, str] = None,
        *,
        request: HttpRequest | None = None,
        context: str | None = None,
        context_object: Model | None = None,
        is_hidden: bool = False,
        plugin_data: dict,
    ) -> "ThreadUpdate": ...


class CreateThreadUpdateHook(
    FilterHook[
        CreateThreadUpdateHookAction,
        CreateThreadUpdateHookFilter,
    ]
):
    """
    This hook wraps a standard Misago function used to create a `ThreadUpdate` object.

    # Example

    The code below implements a custom filter function that stores the actor's IP
    address on the update object:

    ```python
    from django.http import HttpRequest
    from misago.threads.hooks import create_thread_update_hook
    from misago.threads.models import Thread, ThreadUpdate
    from misago.users.models import User


    @create_thread_update_hook.append_filter
    def set_actor_ip_on_thread_update(
        action,
        thread: "Thread",
        action_name: str,
        actor: Union["User", None, str] = None,
        *,
        request: HttpRequest | None = None,
        context: str | None = None,
        context_object: Model | None = None,
        is_hidden: bool = False,
        plugin_data: dict,
    ) -> ThreadUpdate:
        if request:
            plugin_data["actor_id"] = request.user_ip

        return action(
            thread,
            action_name,
            actor,
            request=request,
            context=context,
            context_object=context_object,
            is_hidden=is_hidden,
            plugin_data=plugin_data,
        )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CreateThreadUpdateHookAction,
        thread: "Thread",
        action_name: str,
        actor: Union["User", None, str] = None,
        *,
        request: HttpRequest | None = None,
        context: str | None = None,
        context_object: Model | None = None,
        is_hidden: bool = False,
        plugin_data: dict,
    ) -> "ThreadUpdate":
        return super().__call__(
            action,
            thread,
            action_name,
            actor,
            request=request,
            context=context,
            context_object=context_object,
            is_hidden=is_hidden,
            plugin_data=plugin_data,
        )


create_thread_update_hook = CreateThreadUpdateHook()
