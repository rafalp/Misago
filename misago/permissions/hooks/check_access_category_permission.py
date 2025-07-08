from typing import TYPE_CHECKING, Protocol

from ...categories.models import Category
from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckAccessCategoryPermissionHookAction(Protocol):
    """
    Misago function used to check if a user has permission to access a category
    of unknown type (threads, private threads, or plugin-defined).
    Raises Django’s `Http404` or `PermissionDenied` if they can't.

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


class CheckAccessCategoryPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckAccessCategoryPermissionHookAction`

    Misago function used to check if a user has permission to access
    a category of unknown type (threads, private threads, or plugin-defined).
    Raises Django’s `Http404` or `PermissionDenied` if they can't.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category to check permissions for.
    """

    def __call__(
        self,
        action: CheckAccessCategoryPermissionHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
    ) -> None: ...


class CheckAccessCategoryPermissionHook(
    FilterHook[
        CheckAccessCategoryPermissionHookAction,
        CheckAccessCategoryPermissionHookFilter,
    ]
):
    """
    This hook wraps a standard Misago function used to check if a user has permission
    to access a category of unknown type (threads, private threads, or plugin-defined).
    Raises Django’s `Http404` or `PermissionDenied` if they can't.

    # Example

    The code below implements a custom filter function that blocks a user from seeing
    a specified category if there is a custom flag set on their account.

    ```python
    from django.core.exceptions import PermissionDenied
    from django.utils.translation import pgettext
    from misago.categories.models import Category
    from misago.permissions.hooks import check_access_category_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @check_access_category_permission_hook.append_filter
    def check_user_can_access_category(
        action,
        permissions: UserPermissionsProxy,
        category: Category,
    ) -> None:
        # Run standard permission checks
        action(permissions, category)

        if category.id in permissions.user.plugin_data.get("hidden_category", []):
            raise PermissionDenied(
                pgettext(
                    "category permission error",
                    "Site admin has removed your access to this category."
                )
            )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckAccessCategoryPermissionHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
    ) -> None:
        return super().__call__(action, permissions, category)


check_access_category_permission_hook = CheckAccessCategoryPermissionHook()
