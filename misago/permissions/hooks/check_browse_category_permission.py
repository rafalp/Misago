from typing import TYPE_CHECKING, Protocol

from ...categories.models import Category
from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckBrowseCategoryPermissionHookAction(Protocol):
    """
    A standard Misago function used to check if the user has permission to
    browse a category. It also checks if the user can see the category.
    It raises Django's `Http404` if they can't see it or `PermissionDenied`
    with an error message if they can't browse it.

    # Arguments

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category to check permissions for.

    ## `can_delay: Bool = False`

    A `bool` that specifies if this check can be delayed. If the category can be
    seen by the user but they have no permission to browse it, and both `can_delay`
    and `category.delay_browse_check` are `True`, a `PermissionDenied` error
    will not be raised.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        category: Category,
        can_delay: bool = False,
    ) -> None: ...


class CheckBrowseCategoryPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckBrowseCategoryPermissionHookAction`

    A standard Misago function used to check if the user has permission to
    browse a category. It also checks if the user can see the category.
    It raises Django's `Http404` if they can't see it or `PermissionDenied`
    with an error message if they can't browse it.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category to check permissions for.

    ## `can_delay: Bool = False`

    A `bool` that specifies if this check can be delayed. If the category can be
    seen by the user but they have no permission to browse it, and both `can_delay`
    and `category.delay_browse_check` are `True`, a `PermissionDenied` error
    will not be raised.
    """

    def __call__(
        self,
        action: CheckBrowseCategoryPermissionHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
        can_delay: bool = False,
    ) -> None: ...


class CheckBrowseCategoryPermissionHook(
    FilterHook[
        CheckBrowseCategoryPermissionHookAction,
        CheckBrowseCategoryPermissionHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to check if the user
    has permission to browse a category. It also checks if the user can see the
    category. It raises Django's `Http404` if they can't see it or `PermissionDenied`
    with an error message if they can't browse it.

    # Example

    The code below implements a custom filter function that blocks a user from
    browsing a specified category if there is a custom flag set on their account.

    ```python
    from django.core.exceptions import PermissionDenied
    from django.utils.translation import pgettext
    from misago.categories.models import Category
    from misago.permissions.hooks import check_browse_category_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @check_browse_category_permission_hook.append_filter
    def check_user_can_browse_category(
        action,
        permissions: UserPermissionsProxy,
        category: Category,
    ) -> None:
        # Run standard permission checks
        action(permissions, category)

        if category.id in permissions.user.plugin_data.get("banned_categories", []):
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
        action: CheckBrowseCategoryPermissionHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
        can_delay: bool = False,
    ) -> None:
        return super().__call__(action, permissions, category, can_delay)


check_browse_category_permission_hook = CheckBrowseCategoryPermissionHook()
