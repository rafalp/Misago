from typing import TYPE_CHECKING, Protocol

from ...categories.models import Category
from ...plugins.hooks import FilterHook
from ...threads.models import Post, Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckSeePostLikesPermissionHookAction(Protocol):
    """
    Misago function used to check if a user has permission to see post likes.
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


class CheckSeePostLikesPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckSeePostLikesPermissionHookAction`

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
        action: CheckSeePostLikesPermissionHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
        post: Post,
    ) -> None: ...


class CheckSeePostLikesPermissionHook(
    FilterHook[
        CheckSeePostLikesPermissionHookAction,
        CheckSeePostLikesPermissionHookFilter,
    ]
):
    """
    This hook wraps a standard Misago function used to check if a user has permission
    to see post likes. Raises Django's `PermissionDenied` if they don't.

    # Example

    The code below implements a custom filter function that blocks a user from
    seeing a specific post's likes if it has a flag.

    ```python
    from django.core.exceptions import PermissionDenied
    from django.utils.translation import pgettext
    from misago.categories.models import Category
    from misago.permissions.hooks import check_see_post_likes_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.threads.models import Post, Thread

    @check_see_post_likes_permission_hook.append_filter
    def check_user_can_see_post_likes(
        action,
        permissions: UserPermissionsProxy,
        category: Category,
        thread: Thread,
        post: Post,
    ) -> None:
        # Run standard permission checks
        action(permissions, category, thread, post)

        if post.plugin_data.get("hide_likes"):
            raise PermissionDenied(
                pgettext(
                    "likes permission error",
                    "You can't see this post's likes."
                )
            )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckSeePostLikesPermissionHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
        post: Post,
    ) -> None:
        return super().__call__(action, permissions, category, thread, post)


check_see_post_likes_permission_hook = CheckSeePostLikesPermissionHook()
