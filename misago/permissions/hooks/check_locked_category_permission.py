from typing import TYPE_CHECKING, Protocol

from ...categories.models import Category
from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckLockedCategoryPermissionHookAction(Protocol):
    """
    Misago function used to check if the user has permission to
    post in a closed category. It raises Django's `PermissionDenied` with an
    error message if category is closed and they can't post in it.

    # Arguments

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category to check permissions for.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        category: Category,
    ) -> None: ...


class CheckLockedCategoryPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckLockedCategoryPermissionHookAction`

    Misago function used to check if the user has permission to
    post in a closed category. It raises Django's `PermissionDenied` with an
    error message if category is closed and they can't post in it.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category to check permissions for.
    """

    def __call__(
        self,
        action: CheckLockedCategoryPermissionHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
    ) -> None: ...


class CheckLockedCategoryPermissionHook(
    FilterHook[
        CheckLockedCategoryPermissionHookAction,
        CheckLockedCategoryPermissionHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to check if the user
    has permission to post in a closed category. It raises Django's `PermissionDenied`
    with an error message if category is closed and they can't post in it.

    # Example

    The code below implements a custom filter function that permits a user to
    post in the specific category if they have a custom flag set on their account.

    ```python
    from misago.categories.models import Category
    from misago.permissions.hooks import check_locked_category_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @check_locked_category_permission_hook.append_filter
    def check_user_can_post_in_closed_category(
        action,
        permissions: UserPermissionsProxy,
        category: Category,
    ) -> None:
        user = permissions.user
        if user.is_authenticated:
            post_in_closed_categories = (
                user.plugin_data.get("post_in_closed_categories") or []
            )
        else:
            post_in_closed_categories = None

        if (
            not post_in_closed_categories
            or category.id not in post_in_closed_categories
        ):
            action(permissions, category)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckLockedCategoryPermissionHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
    ) -> None:
        return super().__call__(action, permissions, category)


check_locked_category_permission_hook = CheckLockedCategoryPermissionHook()
