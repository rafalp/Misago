from typing import TYPE_CHECKING, Protocol

from django.db.models import QuerySet

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class FilterPrivateThreadEventsQuerysetHookAction(Protocol):
    """
    Misago function used to set filters on a queryset used to retrieve
    specified private thread's events that user can see.

    # Arguments

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `thread: Thread`

    A private thread instance which's events are retrieved.

    ## `queryset: Queryset`

    A queryset returning thread's events.

    ## Return value

    A `queryset` filtered to show only thread events that the user can see.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        thread: Thread,
        queryset: QuerySet,
    ) -> QuerySet: ...


class FilterPrivateThreadEventsQuerysetHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: FilterPrivateThreadEventsQuerysetHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `thread: Thread`

    A private thread instance which's events are retrieved.

    ## `queryset: Queryset`

    A queryset returning thread's events.

    ## Return value

    A `queryset` filtered to show only thread events that the user can see.
    """

    def __call__(
        self,
        action: FilterPrivateThreadEventsQuerysetHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
        queryset: QuerySet,
    ) -> QuerySet: ...


class FilterPrivateThreadEventsQuerysetHook(
    FilterHook[
        FilterPrivateThreadEventsQuerysetHookAction,
        FilterPrivateThreadEventsQuerysetHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses set filters on private
    thread's events queryset to limit it only to events that the user can see.

    # Example

    The code below implements a custom filter function
    that hides events for user who is not the private thread's owner.

    ```python
    from misago.permissions.hooks import filter_private_thread_events_queryset_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @filter_private_thread_events_queryset_hook.append_filter
    def hide_private_thread_events_from_non_owner(
        action,
        permissions: UserPermissionsProxy,
        thread,
        queryset,
    ) -> None:
        queryset = action(permissions, thread, queryset)

        if permissions.user.id != thread.private_thread_owner_id:
            return queryset.none()

        return queryset
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: FilterPrivateThreadEventsQuerysetHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
        queryset: QuerySet,
    ) -> QuerySet:
        return super().__call__(action, permissions, thread, queryset)


filter_private_thread_events_queryset_hook = FilterPrivateThreadEventsQuerysetHook()
