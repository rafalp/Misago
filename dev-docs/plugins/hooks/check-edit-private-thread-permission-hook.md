# `check_edit_private_thread_permission_hook`

This hook wraps the standard function that Misago uses to check if the user has permission to edit a private thread. It raises Django's `PermissionDenied` with an error message if they can't edit it.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_edit_private_thread_permission_hook
```


## Filter

```python
def custom_check_edit_private_thread_permission_filter(
    action: CheckEditPrivateThreadPermissionHookAction,
    permissions: 'UserPermissionsProxy',
    thread: Thread,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckEditPrivateThreadPermissionHookAction`

A standard Misago function used to check if the user has permission to edit a private thread. It raises Django's `PermissionDenied` with an error message if they can't edit it.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `thread: Thread`

A thread to check permissions for.


## Action

```python
def check_edit_private_thread_permission_action(
    permissions: 'UserPermissionsProxy', thread: Thread
) -> None:
    ...
```

A standard Misago function used to check if the user has permission to edit a private thread. It raises Django's `PermissionDenied` with an error message if they can't edit it.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `thread: Thread`

A thread to check permissions for.


## Example

The code below implements a custom filter function that prevents a user from editing a thread if it's title contains a special prefix.

```python
from django.core.exceptions import PermissionDenied
from misago.permissions.hooks import check_edit_private_thread_permission_hook
from misago.permissions.proxy import UserPermissionsProxy
from misago.threads.models import Thread

@check_edit_private_thread_permission_hook.append_filter
def check_user_can_edit_thread(
    action,
    permissions: UserPermissionsProxy,
    thread: Thread,
) -> None:
    action(permissions, thread)

    if (
        thread.title.startswith("[MVP]")
        and not permissions.is_private_threads_moderator
    ):
        raise PermissionError("Only a moderator can edit this thread.")
```