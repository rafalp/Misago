from typing import TYPE_CHECKING, Protocol

from ...categories.models import Category
from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckAccessThreadPermissionHookAction(Protocol):
    """
    Misago function used to check if a user has permission to access
    a thread of any type (threads, private threads, or plugin-defined).
    Raises Django's `Http404` or `PermissionDenied` if they don't.

    # Arguments

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category to check permissions for.

    ## `thread: Thread`

    A thread to check permissions for.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
    ) -> None: ...


class CheckAccessThreadPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckAccessThreadPermissionHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category to check permissions for.

    ## `thread: Thread`

    A thread to check permissions for.
    """

    def __call__(
        self,
        action: CheckAccessThreadPermissionHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
    ) -> None: ...


class CheckAccessThreadPermissionHook(
    FilterHook[
        CheckAccessThreadPermissionHookAction,
        CheckAccessThreadPermissionHookFilter,
    ]
):
    """
    This hook wraps a standard Misago function used to check if a user has permission
    to access a thread of any type (threads, private threads, or plugin-defined).
    Raises Django's `Http404` or `PermissionDenied` if they don't.

    # Example

    The code below implements a custom filter function that blocks a user from seeing
    a specified thread if there is a custom flag set on their account.

    ```python
    from django.core.exceptions import PermissionDenied
    from django.utils.translation import pgettext
    from misago.categories.models import Category
    from misago.permissions.hooks import check_access_thread_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.threads.models import Thread

    @check_access_thread_permission_hook.append_filter
    def check_user_can_access_thread(
        action,
        permissions: UserPermissionsProxy,
        category: Category,
        thread: Thread,
    ) -> None:
        # Run standard permission checks
        action(permissions, category, thread)

        if thread.id in permissions.user.plugin_data.get("hidden_threads", []):
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
        action: CheckAccessThreadPermissionHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
    ) -> None:
        return super().__call__(action, permissions, category, thread)


check_access_thread_permission_hook = CheckAccessThreadPermissionHook()
