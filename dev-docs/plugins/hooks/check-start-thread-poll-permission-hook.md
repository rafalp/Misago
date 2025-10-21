# `check_start_thread_poll_permission_hook`

This hook allows plugins to replace or extend the permission check for the "can start poll in thread" permission.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_start_thread_poll_permission_hook
```


## Filter

```python
def custom_check_start_thread_poll_permission_filter(
    action: CheckStartThreadPollPermissionHookAction,
    permissions: 'UserPermissionsProxy',
    category: Category,
    thread: Thread,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckStartThreadPollPermissionHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category to check permissions for.


#### `thread: Thread`

A thread to check permissions for.


## Action

```python
def check_start_thread_poll_permission_action(
    permissions: 'UserPermissionsProxy',
    category: Category,
    thread: Thread,
) -> None:
    ...
```

Misago function used to check if the user has permission to start a poll in a thread. Raises Django's `PermissionDenied` exception with an error message if the user lacks permission.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category to check permissions for.


#### `thread: Thread`

A thread to check permissions for.


## Example

Prevents a user from starting a poll in a thread if it is older than 15 days.

```python
from datetime import timedelta

from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.translation import pgettext
from misago.categories.models import Category
from misago.threads.models import Thread
from misago.permissions.hooks import check_start_thread_poll_permission_hook
from misago.permissions.proxy import UserPermissionsProxy

@check_start_thread_poll_permission_hook.append_filter
def check_user_can_start_poll(
    action,
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
) -> None:
    # Run standard permission checks
    action(permissions, category, thread)

    if thread.started_at < timezone.now() - timedelta(days=15):
        raise PermissionDenied(
            pgettext(
                "poll permission error",
                "You can't start polls in threads that are older than 15 days."
            )
        )
```