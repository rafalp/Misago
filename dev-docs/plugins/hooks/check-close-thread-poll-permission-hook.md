# `check_close_thread_poll_permission_hook`

This hook allows plugins to replace or extend the permission check for the "can close thread poll" permission.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_close_thread_poll_permission_hook
```


## Filter

```python
def custom_check_close_thread_poll_permission_filter(
    action: CheckCloseThreadPollPermissionHookAction,
    permissions: 'UserPermissionsProxy',
    category: Category,
    thread: Thread,
    poll: Poll,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckCloseThreadPollPermissionHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category to check permissions for.


#### `thread: Thread`

A thread to check permissions for.


#### `poll: Poll`

A poll to check permissions for.


## Action

```python
def check_close_thread_poll_permission_action(
    permissions: 'UserPermissionsProxy',
    category: Category,
    thread: Thread,
    poll: Poll,
) -> None:
    ...
```

Misago function used to check if the user has permission to close a thread poll. Raises Django's `PermissionDenied` exception with an error message if the user lacks permission.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category to check permissions for.


#### `thread: Thread`

A thread to check permissions for.


#### `poll: Poll`

A poll to check permissions for.


## Example

Prevents a user from closing a poll in a thread if it has more than 5 votes.

```python
from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext
from misago.categories.models import Category
from misago.polls.models import Poll
from misago.threads.models import Thread
from misago.permissions.hooks import check_close_thread_poll_permission_hook
from misago.permissions.proxy import UserPermissionsProxy

@check_close_thread_poll_permission_hook.append_filter
def check_user_can_close_poll(
    action,
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    poll: Poll,
) -> None:
    # Run standard permission checks
    action(permissions, category, thread, poll)

    if poll.votes > 5:
        raise PermissionDenied(
            pgettext(
                "poll permission error",
                "You cannot close polls that have received more than 5 votes."
            )
        )
```