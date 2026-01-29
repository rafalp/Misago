# `check_see_private_thread_permission_hook`

This hook wraps a standard Misago function used to check if the user has a permission to see a private thread. Raises Django's `Http404` if they don't.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_see_private_thread_permission_hook
```


## Filter

```python
def custom_check_see_private_thread_permission_filter(
    action: CheckSeePrivateThreadPermissionHookAction,
    permissions: 'UserPermissionsProxy',
    thread: Thread,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckSeePrivateThreadPermissionHookAction`

Misago function used to check if the user has a permission to see a private thread. Raises Django's `Http404` if they don't.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `thread: Thread`

A thread to check permissions for.


## Action

```python
def check_see_private_thread_permission_action(
    permissions: 'UserPermissionsProxy', thread: Thread
) -> None:
    ...
```

Misago function used to check if the user has a permission to see a private thread. Raises Django's `Http404` if they don't.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `thread: Thread`

A thread to check permissions for.


## Example

The code below implements a custom filter function that blocks a user from seeing a specified thread if there is a custom flag set on their account.

```python
from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext
from misago.permissions.hooks import check_see_private_thread_permission_hook
from misago.permissions.proxy import UserPermissionsProxy
from misago.threads.models import Thread

@check_see_private_thread_permission_hook.append_filter
def check_user_can_see_thread(
    action,
    permissions: UserPermissionsProxy,
    thread: Thread,
) -> None:
    # Run standard permission checks
    action(permissions, category, thread)

    if thread.id in permissions.user.plugin_data.get("banned_thread", []):
        raise PermissionDenied(
            pgettext(
                "thread permission error",
                "Site admin has removed your access to this thread."
            )
        )
```