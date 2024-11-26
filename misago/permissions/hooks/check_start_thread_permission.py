from typing import TYPE_CHECKING, Protocol

from ...categories.models import Category
from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckStartThreadInCategoryPermissionHookAction(Protocol):
    """
    A standard Misago function used to check if the user has permission to
    start a new thread in a category. It raises Django's `PermissionDenied` with
    an error message if they can't start thread in a category.

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


class CheckStartThreadInCategoryPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckStartThreadInCategoryPermissionHookAction`

    A standard Misago function used to check if the user has permission to
    start a new thread in a category. It raises Django's `PermissionDenied` with
    an error message if they can't start thread in a category.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category to check permissions for.
    """

    def __call__(
        self,
        action: CheckStartThreadInCategoryPermissionHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
    ) -> None: ...


class CheckStartThreadInCategoryPermissionHook(
    FilterHook[
        CheckStartThreadInCategoryPermissionHookAction,
        CheckStartThreadInCategoryPermissionHookFilter,
    ]
):
    """
    This hook wraps the standard Misago function used to check if the user has
    permission to start a new thread in a category. It raises Django's
    `PermissionDenied` with an error message if they can't start thread in a category.

    # Example

    The code below implements a custom filter function that prevents the user from
    starting a thread in category if their account is newer than 7 days.

    ```python
    from datetime import timedelta

    from django.core.exceptions import PermissionDenied
    from django.utils import timezone
    from misago.categories.models import Category
    from misago.permissions.hooks import check_start_thread_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @check_start_thread_permission_hook.append_filter
    def check_user_can_start_thread(
        action,
        permissions: UserPermissionsProxy,
        category: Category,
    ) -> None:
        action(permissions, category)

        user = permissions.user
        if (
            user.is_authenticated
            and user.joined_on > timezone.now() - timedelta(days=7):
        ):
            raise PermissionDenied(
                "Your account was created less than 7 days ago. "
                "You can't start threads yet."
            )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckStartThreadInCategoryPermissionHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
    ) -> None:
        return super().__call__(action, permissions, category)


check_start_thread_permission_hook = CheckStartThreadInCategoryPermissionHook()
