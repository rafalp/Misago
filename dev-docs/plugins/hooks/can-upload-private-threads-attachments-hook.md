# `can_upload_private_threads_attachments_hook`

This hook wraps the standard Misago function that checks whether a user has permission to upload attachments in private threads.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import can_upload_private_threads_attachments_hook
```


## Filter

```python
def custom_can_upload_private_threads_attachments_filter(
    action: CanUploadPrivateThreadsAttachmentsHookAction,
    permissions: 'UserPermissionsProxy',
) -> bool:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CanUploadPrivateThreadsAttachmentsHookAction`

A standard Misago function that checks whether a user has permission to upload attachments in private threads.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


### Return value

`True` if a user can upload attachments in a category, and `False` if they cannot.


## Action

```python
def can_upload_private_threads_attachments_action(permissions: 'UserPermissionsProxy') -> bool:
    ...
```

A standard Misago function that checks whether a user has permission to upload attachments in private threads.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


### Return value

`True` if a user can upload attachments in a category, and `False` if they cannot.


## Example

The code below implements a custom filter function that prevents a user from uploading attachments in private threads if a custom flag is set on their account.

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