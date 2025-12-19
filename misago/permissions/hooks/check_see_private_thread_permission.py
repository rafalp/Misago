from typing import TYPE_CHECKING, Protocol

from ...categories.models import Category
from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckSeePrivateThreadPermissionHookAction(Protocol):
    """
    Misago function used to check if the user has a permission to see
    a private thread. Raises Django's `Http404` if they don't.

    # Arguments

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `thread: Thread`

    A thread to check permissions for.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None: ...


class CheckSeePrivateThreadPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckSeePrivateThreadPermissionHookAction`

    Misago function used to check if the user has a permission to see
    a private thread. Raises Django's `Http404` if they don't.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `thread: Thread`

    A thread to check permissions for.
    """

    def __call__(
        self,
        action: CheckSeePrivateThreadPermissionHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None: ...


class CheckSeePrivateThreadPermissionHook(
    FilterHook[
        CheckSeePrivateThreadPermissionHookAction,
        CheckSeePrivateThreadPermissionHookFilter,
    ]
):
    """
    This hook wraps a standard Misago function used to check if the user has
    a permission to see a private thread. Raises Django's `Http404` if they don't.

    # Example

    The code below implements a custom filter function that blocks a user from seeing
    a specified thread if there is a custom flag set on their account.

    ```python
    from django.core.exceptions import PermissionDenied
    from django.utils.translation import pgettext
    from misago.permissions.hooks import check_see_private_thread_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.threads.models import Thread

    @check_see_private_thread_permission_hook.append_filter
    def check_user_can_see_thread(
        action,
        permissions: UserPermissionsProxy,
        thread: Thread,
    ) -> None:
        # Run standard permission checks
        action(permissions, category, thread)

        if thread.id in permissions.user.plugin_data.get("banned_thread", []):
            raise PermissionDenied(
                pgettext(
                    "thread permission error",
                    "Site admin has removed your access to this thread."
                )
            )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckSeePrivateThreadPermissionHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None:
        return super().__call__(action, permissions, thread)


check_see_private_thread_permission_hook = CheckSeePrivateThreadPermissionHook()
