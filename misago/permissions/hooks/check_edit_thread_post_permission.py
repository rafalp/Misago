from typing import TYPE_CHECKING, Protocol

from ...categories.models import Category
from ...plugins.hooks import FilterHook
from ...threads.models import Post, Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckEditThreadPostPermissionHookAction(Protocol):
    """
    Misago function used to check if the user has permission to
    edit a post in a thread. It raises Django's `PermissionDenied` with an
    error message if they don't.

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


class CheckEditThreadPostPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckEditThreadPostPermissionHookAction`

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
        action: CheckEditThreadPostPermissionHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
        post: Post,
    ) -> None: ...


class CheckEditThreadPostPermissionHook(
    FilterHook[
        CheckEditThreadPostPermissionHookAction,
        CheckEditThreadPostPermissionHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to check if the user
    has permission to edit a post in a thread. It raises Django's
    `PermissionDenied` with an error message if they don't.

    # Example

    The code below implements a custom filter function that prevents a user from
    editing a post if it contains a special string.

    ```python
    from django.core.exceptions import PermissionDenied
    from misago.categories.models import Category
    from misago.permissions.hooks import check_edit_thread_post_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.threads.models import Post, Thread

    @check_edit_thread_post_permission_hook.append_filter
    def check_user_can_edit_thread_post(
        action,
        permissions: UserPermissionsProxy,
        category: Category,
        thread: Thread,
        post: Post,
    ) -> None:
        action(permissions, category, thread, post)

        if (
            "[PROTECT]" in post.original
            and not (
                permissions.is_global_moderator
                or permissions.is_category_moderator(thread.category_id)
            )
        ):
            raise PermissionError("Only a moderator can edit this post.")
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckEditThreadPostPermissionHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
        post: Post,
    ) -> None:
        return super().__call__(action, permissions, category, thread, post)


check_edit_thread_post_permission_hook = CheckEditThreadPostPermissionHook()
