from typing import TYPE_CHECKING, Protocol

from ...categories.models import Category
from ...plugins.hooks import FilterHook
from ...threads.models import Post, Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckSeePostEditHistoryPermissionHookAction(Protocol):
    """
    Misago function used to check if a user has permission to see post edit history.
    Raises Django's `PermissionDenied` if they don't.

    # Arguments

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category to check permissions for.

    ## `thread: Thread`

    A thread to check permissions for.

    ## `post: Post`

    A post to check permissions for.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
        post: Post,
    ) -> None: ...


class CheckSeePostEditHistoryPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckSeePostEditHistoryPermissionHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category to check permissions for.

    ## `thread: Thread`

    A thread to check permissions for.

    ## `post: Post`

    A post to check permissions for.
    """

    def __call__(
        self,
        action: CheckSeePostEditHistoryPermissionHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
        post: Post,
    ) -> None: ...


class CheckSeePostEditHistoryPermissionHook(
    FilterHook[
        CheckSeePostEditHistoryPermissionHookAction,
        CheckSeePostEditHistoryPermissionHookFilter,
    ]
):
    """
    This hook wraps the standard Misago function used to check whether a user has
    permission to see a post's edit history.
    Raises Django's `PermissionDenied` if they don't.

    # Example

    The code below implements a custom filter function that blocks a user from
    seeing a specific post's edit history if it has a flag.

    ```python
    from django.core.exceptions import PermissionDenied
    from django.utils.translation import pgettext
    from misago.categories.models import Category
    from misago.permissions.hooks import check_see_post_edit_history_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.threads.models import Post, Thread

    @check_see_post_edit_history_permission_hook.append_filter
    def check_user_can_see_post_edits(
        action,
        permissions: UserPermissionsProxy,
        category: Category,
        thread: Thread,
        post: Post,
    ) -> None:
        # Run standard permission checks
        action(permissions, category, thread, post)

        if post.plugin_data.get("hide_edits"):
            raise PermissionDenied(
                pgettext(
                    "edits permission error",
                    "You can't see this post's edits."
                )
            )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckSeePostEditHistoryPermissionHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
        post: Post,
    ) -> None:
        return super().__call__(action, permissions, category, thread, post)


check_see_post_edit_history_permission_hook = CheckSeePostEditHistoryPermissionHook()
