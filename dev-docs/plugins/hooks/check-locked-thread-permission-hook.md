# `check_locked_thread_permission_hook`

This hook allows plugins to extend or replace the logic for checking whether a user has permission to bypass a thread's locked status.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_locked_thread_permission_hook
```


## Filter

```python
def custom_check_locked_thread_permission_filter(
    action: CheckLockedThreadPermissionHookAction,
    permissions: 'UserPermissionsProxy',
    thread: Thread,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckLockedThreadPermissionHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `thread: Thread`

A thread to check permissions for.


## Action

```python
def check_locked_thread_permission_action(
    permissions: 'UserPermissionsProxy', thread: Thread
) -> None:
    ...
```

Misago function that checks whether a user has permission to bypass a thread's locked status. Raises `PermissionDenied` if they don't.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `thread: Thread`

A thread to check permissions for.


## Example

The code below implements a custom filter function that permits a user to post in the specific thread if they have a custom flag set on their account.

```python
from misago.permissions.hooks import check_locked_thread_permission_hook
from misago.permissions.proxy import UserPermissionsProxy
from misago.threads.models import Thread

@check_locked_thread_permission_hook.append_filter
def check_user_can_post_in_locked_thread(
    action,
    permissions: UserPermissionsProxy,
    thread: Thread,
) -> None:
    user = permissions.user
    if user.is_authenticated:
        post_in_locked_threads = (
            user.plugin_data.get("post_in_locked_threads") or []
        )
    else:
        post_in_locked_threads = None

    if (
        not post_in_locked_threads
        or thread.id not in post_in_locked_threads
    ):
        action(permissions, thread)
```