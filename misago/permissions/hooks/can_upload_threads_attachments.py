from typing import TYPE_CHECKING, Protocol

from ...categories.models import Category
from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CanUploadThreadsAttachmentsHookAction(Protocol):
    """
    A standard Misago function that checks if a user has permission to upload
    attachments in a category.

    # Arguments

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category to check permissions for.

    # Return value

    `True` if a user can upload attachments in a category, and `False` if they cannot.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        category: Category,
    ) -> bool: ...


class CanUploadThreadsAttachmentsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CanUploadThreadsAttachmentsHookAction`

    A standard Misago function that checks if a user has permission to upload
    attachments in a category.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category to check permissions for.

    # Return value

    `True` if a user can upload attachments in a category, and `False` if they cannot.
    """

    def __call__(
        self,
        action: CanUploadThreadsAttachmentsHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
    ) -> bool: ...


class CanUploadThreadsAttachmentsHook(
    FilterHook[
        CanUploadThreadsAttachmentsHookAction,
        CanUploadThreadsAttachmentsHookFilter,
    ]
):
    """
    This hook wraps the standard Misago function that checks whether a user has
    permission to upload attachments in a category.

    # Example

    The code below implements a custom filter function that prevents a user
    from uploading attachments in a specific category if a custom flag is set
    on their account.

    ```python
    from misago.categories.models import Category
    from misago.permissions.hooks import can_upload_threads_attachments_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @can_upload_threads_attachments_hook.append_filter
    def user_can_upload_attachments_in_category(
        action,
        permissions: UserPermissionsProxy,
        category: Category,
    ) -> bool:
        if category.id in permissions.user.plugin_data.get("banned_attachments", []):
            return False

        result action(permissions, category)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CanUploadThreadsAttachmentsHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
    ) -> bool:
        return super().__call__(action, permissions, category)


can_upload_threads_attachments_hook = CanUploadThreadsAttachmentsHook()
