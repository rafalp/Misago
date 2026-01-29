from typing import TYPE_CHECKING, Protocol

from ...categories.models import Category
from ...plugins.hooks import FilterHook
from ...threads.models import Post, Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CanSeePostsLikesCountHookAction(Protocol):
    """
    Misago function used to check if a user has permission to see a post's
    likes count. Returns `True` if they can and `False` if they don't.

    # Arguments

    ## `users: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category to check permissions for.

    ## `thread: Thread`

    A thread to check permissions for.

    ## `post: Post`

    A post to check permissions for.

    # Return value

    A `bool` with `True` if user can see post's likes count, and `False` if
    they can't.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
        post: Post,
    ) -> bool: ...


class CanSeePostsLikesCountHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CanSeePostsLikesCountHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `users: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category to check permissions for.

    ## `thread: Thread`

    A thread to check permissions for.

    ## `post: Post`

    A post to check permissions for.

    # Return value

    A `bool` with `True` if user can see post's likes count, and `False` if
    they can't.
    """

    def __call__(
        self,
        action: CanSeePostsLikesCountHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
        post: Post,
    ) -> bool: ...


class CanSeePostsLikesCountHook(
    FilterHook[
        CanSeePostsLikesCountHookAction,
        CanSeePostsLikesCountHookFilter,
    ]
):
    """
    This hook wraps a standard Misago function used to check if a user has
    permission to see a post's likes count. Returns `True` if they can
    and `False` if they don't.

    # Example

    The code below implements a custom filter function that blocks a user from
    seeing a specific post's likes count if it has a flag.

    ```python
    from django.core.exceptions import PermissionDenied
    from django.utils.translation import pgettext
    from misago.categories.models import Category
    from misago.permissions.hooks import can_see_post_likes_count_hook
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.threads.models import Post, Thread

    @can_see_post_likes_count_hook.append_filter
    def check_user_can_see_post_likes(
        action,
        permissions: UserPermissionsProxy,
        category: Category,
        thread: Thread,
        post: Post,
    ) -> bool:
        if post.plugin_data.get("hide_likes"):
            return False

        return action(permissions, category, thread, post)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CanSeePostsLikesCountHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
        post: Post,
    ) -> bool:
        return super().__call__(action, permissions, category, thread, post)


can_see_post_likes_count_hook = CanSeePostsLikesCountHook()
