# `check_download_attachment_permission_hook`

This hook wraps the standard function that Misago uses to check if the user has permission to download an attachment. It raises Django's `Http404` if the user cannot see the attachment or `PermissionDenied` if they are not allowed to download it.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_download_attachment_permission_hook
```


## Filter

```python
def custom_check_download_attachment_permission_filter(
    action: CheckDownloadAttachmentPermissionHookAction,
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

#### `action: CheckDownloadAttachmentPermissionHookAction`

A standard Misago function used to check if a user has permission to download an attachment. It raises Django's `Http404` if the user cannot see the attachment or `PermissionDenied` if they are not allowed to download it.

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
def check_download_attachment_permission_action(
    permissions: 'UserPermissionsProxy',
    category: Category | None,
    thread: Thread | None,
    post: Post | None,
    attachment: Attachment,
) -> None:
    ...
```

A standard Misago function used to check if a user has permission to download an attachment. It raises Django's `Http404` if the user cannot see the attachment or `PermissionDenied` if they are not allowed to download it.


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

The code below implements a custom filter function that prevents a user from downloading an attachment if its flagged by plugin.

```python
from django.http import Http404
from misago.attachments.models import Attachment
from misago.categories.models import Category
from misago.permissions.hooks import check_download_attachment_permission_hook
from misago.permissions.proxy import UserPermissionsProxy
from misago.threads.models import Post, Thread

@check_download_attachment_permission_hook.append_filter
def check_user_can_download_attachment(
    action,
    permissions: UserPermissionsProxy,
    category: Category | None,
    thread: Thread | None,
    post: Post | None,
    attachment: Attachment,
) -> None:
    action(permissions, category, thread, post, attachment)

    if not (
        attachment.plugin_data.get("hidden")
        and permissions.user.is_authenticated
        and permissions.user.is_misago_admin
    ):
        raise Http404()
```