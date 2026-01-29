from typing import TYPE_CHECKING, Protocol

from ...edits.models import PostEdit
from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckRestorePostEditPermissionHookAction(Protocol):
    """
    Misago function used to check if a user has permission to restore a post
    from a post edit. Raises Django's `PermissionDenied` if they don't.

    # Arguments

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `post_edit: PostEdit`

    A post edit to check permissions for.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        post_edit: PostEdit,
    ) -> None: ...


class CheckRestorePostEditPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckRestorePostEditPermissionHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `post_edit: PostEdit`

    A post edit to check permissions for.
    """

    def __call__(
        self,
        action: CheckRestorePostEditPermissionHookAction,
        permissions: "UserPermissionsProxy",
        post_edit: PostEdit,
    ) -> None: ...


class CheckRestorePostEditPermissionHook(
    FilterHook[
        CheckRestorePostEditPermissionHookAction,
        CheckRestorePostEditPermissionHookFilter,
    ]
):
    """
    This hook wraps the standard Misago function used to check whether a user has
    permission to restore a post from a post edit.
    Raises Django's `PermissionDenied` if they don't.

    # Example

    The code below implements a custom filter function that blocks a user from
    restoring a post from a post edit if it contains disallowed words.

    ```python
    from django.core.exceptions import PermissionDenied
    from django.utils.translation import pgettext
    from misago.edits.models import PostEdit
    from misago.permissions.hooks import check_restore_post_edit_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @check_restore_post_edit_permission_hook.append_filter
    def check_user_can_hide_protected_post_edit(
        action,
        permissions: UserPermissionsProxy,
        post_edit: PostEdit,
    ) -> None:
        # Run standard permission checks
        action(permissions, post_edit)

        if (
            not permissions.is_global_moderator
            and post_edit.old_content
            and "swear" in post_edit.old_content.lower()
        ):
            raise PermissionDenied(
                pgettext(
                    "edits permission error",
                    "You can't restore the post from this edit."
                )
            )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckRestorePostEditPermissionHookAction,
        permissions: "UserPermissionsProxy",
        post_edit: PostEdit,
    ) -> None:
        return super().__call__(action, permissions, post_edit)


check_restore_post_edit_permission_hook = CheckRestorePostEditPermissionHook()
