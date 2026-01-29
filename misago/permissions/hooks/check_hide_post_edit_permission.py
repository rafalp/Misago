from typing import TYPE_CHECKING, Protocol

from ...edits.models import PostEdit
from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckHidePostEditPermissionHookAction(Protocol):
    """
    Misago function used to check if a user has permission to hide a post edit.
    Raises Django's `PermissionDenied` if they don't.

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


class CheckHidePostEditPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckHidePostEditPermissionHookAction`

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
        action: CheckHidePostEditPermissionHookAction,
        permissions: "UserPermissionsProxy",
        post_edit: PostEdit,
    ) -> None: ...


class CheckHidePostEditPermissionHook(
    FilterHook[
        CheckHidePostEditPermissionHookAction,
        CheckHidePostEditPermissionHookFilter,
    ]
):
    """
    This hook wraps the standard Misago function used to check whether a user has
    permission to hide a post edit.
    Raises Django's `PermissionDenied` if they don't.

    # Example

    The code below implements a custom filter function that blocks a user from
    hiding a post edit record if it has a protected flag.

    ```python
    from django.core.exceptions import PermissionDenied
    from django.utils.translation import pgettext
    from misago.edits.models import PostEdit
    from misago.permissions.hooks import check_hide_post_edit_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @check_hide_post_edit_permission_hook.append_filter
    def check_user_can_hide_protected_post_edit(
        action,
        permissions: UserPermissionsProxy,
        post_edit: PostEdit,
    ) -> None:
        # Run standard permission checks
        action(permissions, post_edit)

        if post_edit.plugin_data.get("is_protected"):
            raise PermissionDenied(
                pgettext(
                    "edits permission error",
                    "You can't hide this post edit."
                )
            )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckHidePostEditPermissionHookAction,
        permissions: "UserPermissionsProxy",
        post_edit: PostEdit,
    ) -> None:
        return super().__call__(action, permissions, post_edit)


check_hide_post_edit_permission_hook = CheckHidePostEditPermissionHook()
