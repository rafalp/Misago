from typing import TYPE_CHECKING, Protocol

from ...categories.models import Category
from ...plugins.hooks import FilterHook
from ...threads.models import Post, Thread

if TYPE_CHECKING:
    from ...users.models import User
    from ..proxy import UserPermissionsProxy


class CheckSeeUserProfilePermissionHookAction(Protocol):
    """
    Misago function used to check if a user has permission to see another user's profile.
    Raises Django's PermissionDenied if they don't.

    # Arguments

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `user: User`

    The user whose profile is being accessed.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        user: "User",
    ) -> None: ...


class CheckSeeUserProfilePermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckSeeUserProfilePermissionHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    Misago function used to check if a user has permission to see other user's profile.
    Raises Django's `PermissionDenied` if they don't.

    # Arguments

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `user: User`

    The user whose profile is being accessed.
    """

    def __call__(
        self,
        action: CheckSeeUserProfilePermissionHookAction,
        permissions: "UserPermissionsProxy",
        user: "User",
    ) -> None: ...


class CheckSeeUserProfilePermissionHook(
    FilterHook[
        CheckSeeUserProfilePermissionHookAction,
        CheckSeeUserProfilePermissionHookFilter,
    ]
):
    """
    This hook wraps a Misago function used to check if a user has permission to
    see another user's profile. Raises Django's PermissionDenied if they don't.

    # Example

    Block a user from seeing another user's profile if it's private:

    ```python
    from django.core.exceptions import PermissionDenied
    from django.utils.translation import pgettext
    from misago.permissions.hooks import check_see_user_profile_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.users.models import User

    @check_see_user_profile_permission_hook.append_filter
    def check_user_can_see_user_profile(
        action, permissions: UserPermissionsProxy, user: User
    ) -> None:
        # Run standard permission checks
        action(permissions, user)

        if not user.plugin_data.get("private_profile"):
            return

        if (
            not permissions.user.is_authenticated
            or not permissions.user.plugin_data.get("can_see_private_profiles")
        ):
            raise PermissionDenied(
                pgettext(
                    "user profile permission error",
                    "%(user)s's profile is private.",
                ) % {"user": user.username}
            )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckSeeUserProfilePermissionHookAction,
        permissions: "UserPermissionsProxy",
        user: "User",
    ) -> None:
        return super().__call__(action, permissions, user)


check_see_user_profile_permission_hook = CheckSeeUserProfilePermissionHook()
