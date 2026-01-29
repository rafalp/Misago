# `check_change_private_thread_owner_permission_hook`

This hook allows plugins to extend or replace the logic for checking whether a user has permission to change a private thread's owner.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_change_private_thread_owner_permission_hook
```


## Filter

```python
def custom_check_change_private_thread_owner_permission_filter(
    action: CheckChangePrivateThreadOwnerPermissionHookAction,
    permissions: 'UserPermissionsProxy',
    thread: Thread,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckChangePrivateThreadOwnerPermissionHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.


#### `permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `thread: Thread`

The thread to check permissions for.


## Action

```python
def check_change_private_thread_owner_permission_action(
    permissions: 'UserPermissionsProxy', thread: Thread
) -> None:
    ...
```

Misago function that checks whether a user has permission to change a private thread's owner. Raises `PermissionDenied` if they don't.


### Arguments

#### `permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `thread: Thread`

The thread to check permissions for.


## Example

Prevent a user flagged as a support employee from giving away ownership of a private thread:

```python
from django.core.exceptions import PermissionDenied
from misago.permissions.hooks import check_change_private_thread_owner_permission_hook
from misago.permissions.proxy import UserPermissionsProxy
from misago.threads.models import Thread

@check_change_private_thread_owner_permission_hook.append_filter
def check_user_can_change_private_thread_owner(
    action,
    permissions: UserPermissionsProxy,
    thread: Thread,
) -> None:
    # Run default checks
    action(permissions, thread)

    if (
        not permissions.is_private_threads_moderator
        and permissions.user.plugin_data["support"]
    ):
        raise PermissionDenied("You cant give away a private thread ownership.")
```