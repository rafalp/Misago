from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class GetPrivateThreadsQueriesHookAction(Protocol):
    """
    Standard Misago function used to get the names of predefined `WHERE` clauses
    for use by other functions to retrieve private threads accessible by the user.

    Standard `WHERE` clauses implemented by Misago can be retrieved from the
    `PrivateThreadsQuery` `StrEnum`:

    ```python
    from misago.permissions.enums import PrivateThreadsQuery
    ```

    # Arguments

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    # Return value

    A set of `PrivateThreadsQuery` members.
    When a set contains more than one `PrivateThreadsQuery`, resulting `Q`
    expressions should be `OR` together.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
    ) -> set[str]: ...


class GetPrivateThreadsQueriesHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetPrivateThreadsQueriesHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    # Return value

    A set of `PrivateThreadsQuery` members.
    When a set contains more than one `PrivateThreadsQuery`, resulting `Q`
    expressions should be `OR` together.
    """

    def __call__(
        self,
        action: GetPrivateThreadsQueriesHookAction,
        permissions: "UserPermissionsProxy",
    ) -> set[str]: ...


class GetPrivateThreadsQueriesHook(
    FilterHook[
        GetPrivateThreadsQueriesHookAction,
        GetPrivateThreadsQueriesHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get the names of
    predefined `WHERE` clauses for use by other functions to retrieve private
    threads accessible by the user.

    # Example

    The code below implements a custom filter function that grants the user access
    to all private threads:

    ```python
    from misago.permissions.enums import PrivateThreadsQuery
    from misago.permissions.hooks import get_private_threads_queries_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @get_private_threads_queries_hook.append_filter
    def get_threads_queries(
        action,
        permissions: UserPermissionsProxy,
    ) -> set[str]:
        if permissions.user.plugin_data.get("private_threads_full_access"):
            return PrivateThreadsQuery.ALL

        return action(permissions)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetPrivateThreadsQueriesHookAction,
        permissions: "UserPermissionsProxy",
    ) -> set[str]:
        return super().__call__(action, permissions)


get_private_threads_queries_hook = GetPrivateThreadsQueriesHook()
