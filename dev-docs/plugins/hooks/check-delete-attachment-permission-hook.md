# `check_delete_attachment_permission_hook`

This hook wraps the standard function that Misago uses to check if the user has permission to delete an attachment. It raises `PermissionDenied` if they are not allowed to delete it.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_delete_attachment_permission_hook
```


## Filter

```python
def custom_check_delete_attachment_permission_filter(
    action: CheckDeleteAttachmentPermissionHookAction,
    permissions: 'UserPermissionsProxy',
    category: Category | None,
    thread: Thread | None,
    post: Post | None,
    attachment: Attachment,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckDeleteAttachmentPermissionHookAction`

Misago function used to check if a user has permission to delete an attachment. It raises `PermissionDenied` if they are not allowed to delete it.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category | None`

A category to check permissions for, or `None` if the attachment wasn't posted.


#### `thread: Thread | None`

A thread to check permissions for, or `None` if the attachment wasn't posted.


#### `post: Post | None`

A post to check permissions for, or `None` if the attachment wasn't posted.


#### `attachment: Attachment`

An attachment to check permissions for.


## Action

```python
def check_delete_attachment_permission_action(
    permissions: 'UserPermissionsProxy',
    category: Category | None,
    thread: Thread | None,
    post: Post | None,
    attachment: Attachment,
) -> None:
    ...
```

Misago function used to check if a user has permission to delete an attachment. It raises `PermissionDenied` if they are not allowed to delete it.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category | None`

A category to check permissions for, or `None` if the attachment wasn't posted.


#### `thread: Thread | None`

A thread to check permissions for, or `None` if the attachment wasn't posted.


#### `post: Post | None`

A post to check permissions for, or `None` if the attachment wasn't posted.


#### `attachment: Attachment`

An attachment to check permissions for.


## Example

The code below implements a custom filter function that prevents a user from deleting an attachment if its flagged by plugin.

```python
from django.core.exceptions import PermissionDenied
from misago.attachments.models import Attachment
from misago.categories.models import Category
from misago.permissions.hooks import check_delete_attachment_permission_hook
from misago.permissions.proxy import UserPermissionsProxy
from misago.threads.models import Post, Thread

@check_delete_attachment_permission_hook.append_filter
def check_user_can_delete_protected_attachment(
    action,
    permissions: UserPermissionsProxy,
    category: Category | None,
    thread: Thread | None,
    post: Post | None,
    attachment: Attachment,
) -> None:
    action(permissions, category, thread, post, attachment)

    if not (
        attachment.plugin_data.get("protected")
        and permissions.user.is_authenticated
        and permissions.user.is_misago_admin
    ):
        raise PermissionDenied(
            "This attachment is protected. You can't delete it."
        )
```