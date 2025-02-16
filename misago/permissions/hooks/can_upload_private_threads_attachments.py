from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CanUploadPrivateThreadsAttachmentsHookAction(Protocol):
    """
    A standard Misago function that checks whether a user has permission to
    upload attachments in private threads.

    # Arguments

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    # Return value

    `True` if a user can upload attachments in a category, and `False` if they cannot.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
    ) -> bool: ...


class CanUploadPrivateThreadsAttachmentsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CanUploadPrivateThreadsAttachmentsHookAction`

    A standard Misago function that checks whether a user has permission to
    upload attachments in private threads.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    # Return value

    `True` if a user can upload attachments in a category, and `False` if they cannot.
    """

    def __call__(
        self,
        action: CanUploadPrivateThreadsAttachmentsHookAction,
        permissions: "UserPermissionsProxy",
    ) -> bool: ...


class CanUploadPrivateThreadsAttachmentsHook(
    FilterHook[
        CanUploadPrivateThreadsAttachmentsHookAction,
        CanUploadPrivateThreadsAttachmentsHookFilter,
    ]
):
    """
    This hook wraps the standard Misago function that checks whether a user has
    permission to upload attachments in private threads.

    # Example

    The code below implements a custom filter function that prevents a user
    from uploading attachments in private threads if a custom flag is set
    on their account.

    ```python
    from misago.permissions.hooks import can_upload_threads_attachments_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @can_upload_private_threads_attachments_hook.append_filter
    def user_can_upload_attachments_in_category(
        action,
        permissions: UserPermissionsProxy,
    ) -> bool:
        if permissions.user.plugin_data.get("banned_private_threads_attachments"):
            return False

        result action(permissions)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CanUploadPrivateThreadsAttachmentsHookAction,
        permissions: "UserPermissionsProxy",
    ) -> bool:
        return super().__call__(action, permissions)


can_upload_private_threads_attachments_hook = CanUploadPrivateThreadsAttachmentsHook()
