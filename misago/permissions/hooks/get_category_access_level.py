from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class GetCategoryAccessLevelHookAction(Protocol):
    """
    A standard Misago function used to get a user's access level for a category.
    Access levels are used to build the final threads queryset for thread lists.

    Default levels are:

    - `moderator`: the user is a moderator for this category.
    - `started_only` the user can see only the pinned threads or ones they started.
    - `default`: the user has default access to threads in this category.

    The enum with all access levels is also available:

    ```python
    from misago.permissions.enums import CategoryAccess

    CategoryAccess.MODERATOR
    CategoryAccess.STARTED_ONLY
    CategoryAccess.DEFAULT
    ```

    Plugins can define custom levels by returning a `str` with their value.

    # Arguments

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: dict`

    A `dict` with category data.

    # Return value

    A `CategoryAccess` member or a `str` with a custom access level. If `none`,
    threads from this category are excluded from the threads list.
    """

    def __call__(
        self,
        user_permissions: "UserPermissionsProxy",
        category: dict,
    ) -> str | None: ...


class GetCategoryAccessLevelHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetCategoryAccessLevelHookAction`

    A standard Misago function used to get a user's access level for a category.
    Access levels are used to build the final threads queryset for thread lists.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: dict`

    A `dict` with category data.

    # Return value

    A `CategoryAccess` member or a `str` with a custom access level. If `none`,
    threads from this category are excluded from the threads list.
    """

    def __call__(
        self,
        action: GetCategoryAccessLevelHookAction,
        user_permissions: "UserPermissionsProxy",
        category: dict,
    ) -> str | None: ...


class GetCategoryAccessLevelHook(
    FilterHook[GetCategoryAccessLevelHookAction, GetCategoryAccessLevelHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to get category's access level
    for the user.

    # Example

    The code below implements a custom filter function that specifies a custom access level
    for categories that have special attribute set by the `get_category_data` hook:

    ```python
    from misago.permissions.hooks import get_category_access_level_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @get_category_access_level_hook.append_filter
    def get_category_access_level(
        action,
        user_permissions: UserPermissionsProxy,
        category: dict,
    ) -> str | None:
        if category["special_access"]:
            return "special_level"

        return action(user_permissions, category)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetCategoryAccessLevelHookAction,
        user_permissions: "UserPermissionsProxy",
        category: dict,
    ) -> str | None:
        return super().__call__(action, user_permissions, category)


get_category_access_level_hook = GetCategoryAccessLevelHook()
