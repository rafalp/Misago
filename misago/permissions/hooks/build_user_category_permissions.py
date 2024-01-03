from typing import Protocol

from django.contrib.auth import get_user_model

from ...plugins.hooks import FilterHook

User = get_user_model()


class BuildUserCategoryPermissionsHookAction(Protocol):
    """
    A standard Misago function used to get user permissions.

    Retrieves permissions data from cache or builds new ones.

    # Arguments

    ## `user: User`

    A user to return permissions for.

    ## `cache_versions: dict`

    A Python `dict` with cache versions.

    # Return value

    A Python `dict` with user permissions.
    """

    def __call__(self, user: User, cache_versions: dict) -> dict:
        ...


class BuildUserCategoryPermissionsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: BuildUserCategoryPermissionsHookAction`

    A standard Misago function used to get user permissions or the next filter
    function from another plugin.

    See the [action](#action) section for details.

    ## `groups: list[Group]`

    A list of groups user belongs to.

    # Return value

    A Python `dict` with user permissions build from their groups.
    """

    def __call__(
        self,
        action: BuildUserCategoryPermissionsHookAction,
        user: User,
        cache_versions: dict,
    ) -> dict:
        ...


class BuildUserCategoryPermissionsHook(
    FilterHook[
        BuildUserCategoryPermissionsHookAction, BuildUserCategoryPermissionsHookFilter
    ]
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
    from misago.permissions.hooks import build_user_permissions_hook
    from misago.users.models import User


    @get_user_permissions_hook.append_filter
    def include_plugin_permission(
        action, user: User, cache_versions: dict
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
        action: BuildUserCategoryPermissionsHookAction,
        user: User,
        cache_versions: dict,
    ) -> dict:
        return super().__call__(action, user, cache_versions)


build_user_category_permissions_hook = BuildUserCategoryPermissionsHook()
