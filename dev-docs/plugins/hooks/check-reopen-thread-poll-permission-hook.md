# `check_reopen_thread_poll_permission_hook`

This hook allows plugins to replace or extend the permission check for the "can reopen closed thread poll" permission.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_reopen_thread_poll_permission_hook
```


## Filter

```python
def custom_check_reopen_thread_poll_permission_filter(
    action: CheckReopenThreadPollPermissionHookAction,
    permissions: 'UserPermissionsProxy',
    category: Category,
    thread: Thread,
    poll: Poll,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckReopenThreadPollPermissionHookAction`

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
def check_reopen_thread_poll_permission_action(
    permissions: 'UserPermissionsProxy',
    category: Category,
    thread: Thread,
    poll: Poll,
) -> None:
    ...
```

A standard Misago function used to check if the user has permission to reopen a closed thread poll. Raises Django's `PermissionDenied` exception with an error message if the user lacks permission.


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

Allows user to reopen their own poll in a thread if it has no votes.

```python
from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext
from misago.categories.models import Category
from misago.polls.models import Poll
from misago.threads.models import Thread
from misago.permissions.checkutils import check_permissions
from misago.permissions.hooks import check_reopen_thread_poll_permission_hook
from misago.permissions.proxy import UserPermissionsProxy

@check_reopen_thread_poll_permission_hook.append_filter
def check_user_can_reopen_poll(
    action,
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    poll: Poll,
) -> None:
    with check_permissions() as can_reopen_poll:
        action(permissions, category, thread, poll)

    if can_reopen_poll:
        return

    if (
        not permissions.user.id
        or not poll.starter_id
        or permissions.user.id != poll.starter_id
    ):
        raise PermissionDenied(
            pgettext(
                "poll permission error",
                "You can't reopen other users polls."
            )
        )

    if poll.votes:
        raise PermissionDenied(
            pgettext(
                "poll permission error",
                "You can't reopen polls that somebody has voted in."
            )
        )
```