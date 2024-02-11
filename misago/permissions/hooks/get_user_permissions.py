from typing import Protocol

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from ...plugins.hooks import FilterHook

User = get_user_model()


class GetUserPermissionsHookAction(Protocol):
    """
    A standard Misago function used to get user permissions.

    Retrieves permissions data from cache or builds new ones.

    # Arguments

    ## `user: User | AnonymousUser`

    A user to return permissions for.

    ## `cache_versions: dict`

    A Python `dict` with cache versions.

    # Return value

    A Python `dict` with user permissions.
    """

    def __call__(self, user: User | AnonymousUser, cache_versions: dict) -> dict: ...


class GetUserPermissionsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetUserPermissionsHookAction`

    A standard Misago function used to get user permissions or the next filter
    function from another plugin.

    See the [action](#action) section for details.

    ## `user: User | AnonymousUser`

    A user to return permissions for.

    ## `cache_versions: dict`

    A Python `dict` with cache versions.

    # Return value

    A Python `dict` with user permissions.
    """

    def __call__(
        self,
        action: GetUserPermissionsHookAction,
        user: User | AnonymousUser,
        cache_versions: dict,
    ) -> dict: ...


class GetUserPermissionsHook(
    FilterHook[GetUserPermissionsHookAction, GetUserPermissionsHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to get user permissions.

    User permissions are a Python `dict`. This `dict` is first retrieved from the cache,
    and if that fails, a new `dict` is built from the user's groups.

    Plugins can use this hook to make additional changes to the final Python `dict`
    based on user data.

    # Example

    The code below implements a custom filter function that includes a custom
    permission into the final user permissions, retrieved from their
    `plugin_data` attribute:

    ```python
    from django.contrib.auth.models import AnonymousUser
    from misago.permissions.hooks import build_user_permissions_hook
    from misago.users.models import User


    @get_user_permissions_hook.append_filter
    def include_plugin_permission(
        action, user: User | AnonymousUser, cache_versions: dict
    ) -> dict:
        permissions = action(user, cache_versions)
        permissions["plugin_permission"] = False

        if user.plugin_data.get("plugin_permission"):
            permissions["plugin_permission"] = True

        return permissions
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetUserPermissionsHookAction,
        user: User | AnonymousUser,
        cache_versions: dict,
    ) -> dict:
        return super().__call__(action, user, cache_versions)


get_user_permissions_hook = GetUserPermissionsHook()
