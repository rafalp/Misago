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

    ## `context: str | None = None`

    A `str` with context, e.g., a previous thread title or the name of
    `context_object`. `None` if not available or not used for this `action_name`.

    ## `context_object: Model | None = None`

    A `Model` instance that this update object should store a generic relation to.

    ## `is_hidden: bool = False`

    Controls whether the newly created update should be hidden. Hidden updates
    are only visible to moderators but can be made visible to all users.
    Defaults to `False`.

    ## `commit: bool = True`

    A `bool` indicating whether the new `ThreadUpdate` instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.

    # Return value

    A newly created `ThreadUpdate` instance.
    """

    def __call__(
        self,
        thread: "Thread",
        action_name: str,
        actor: Union["User", None, str] = None,
        *,
        context: str | None = None,
        context_object: Model | None = None,
        is_hidden: bool = False,
        commit: bool = True,
        request: HttpRequest | None = None,
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

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.

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
        context: str | None = None,
        context_object: Model | None = None,
        is_hidden: bool = False,
        commit: bool = True,
        request: HttpRequest | None = None,
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
    from misago.threadupdates.hooks import create_thread_update_hook
    from misago.threadupdates.models import ThreadUpdate


    @create_thread_update_hook.append_filter
    def set_actor_ip_on_thread_update(
        action,
        *args,
        commit: bool = True,
        request: HttpRequest | None = None,
        **kwargs
    ) -> ThreadUpdate:
        if request:
            plugin_data["actor_id"] = request.user_ip

        thread_update = action(
            *args,
            commit=False,
            request=request,
            **kwargs
        )

        if request:
            thread_update.plugin_data["actor_id"] = request.user_ip

        if commit:
            thread_update.save()

        return thread_update
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
        context: str | None = None,
        context_object: Model | None = None,
        is_hidden: bool = False,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> "ThreadUpdate":
        return super().__call__(
            action,
            thread,
            action_name,
            actor,
            context=context,
            context_object=context_object,
            is_hidden=is_hidden,
            commit=commit,
            request=request,
        )


create_thread_update_hook = CreateThreadUpdateHook()
