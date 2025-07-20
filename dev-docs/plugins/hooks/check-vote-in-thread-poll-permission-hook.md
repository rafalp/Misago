# `check_vote_in_thread_poll_permission_hook`

This hook allows plugins to replace or extend the permission check for the "can vote in thread poll" permission.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_vote_in_thread_poll_permission_hook
```


## Filter

```python
def custom_check_vote_in_thread_poll_permission_filter(
    action: CheckVoteInThreadPollPermissionHookAction,
    permissions: 'UserPermissionsProxy',
    category: Category,
    thread: Thread,
    poll: Poll,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckVoteInThreadPollPermissionHookAction`

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
def check_vote_in_thread_poll_permission_action(
    permissions: 'UserPermissionsProxy',
    category: Category,
    thread: Thread,
    poll: Poll,
) -> None:
    ...
```

Misago function used to check if the user has permission to vote in a thread poll. Raises Django's `PermissionDenied` exception with an error message if the user lacks permission.


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

Prevents a user from voting in a poll if their account has less than 20 days.

```python
from datetime import timedelta

from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.translation import pgettext
from misago.categories.models import Category
from misago.polls.models import Poll
from misago.threads.models import Thread
from misago.permissions.hooks import check_vote_in_thread_poll_permission_hook
from misago.permissions.proxy import UserPermissionsProxy

@check_vote_in_thread_poll_permission_hook.append_filter
def check_user_can_vote_in_poll(
    action,
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    poll: Poll,
) -> None:
    # Run standard permission checks
    action(permissions, category, thread, poll)

    min_user_age = timezone.now() - timedelta(days=20)
    if permissions.user.is_anonymous or permissions.user.joined_on < min_user_age:
        raise PermissionDenied(
            pgettext(
                "poll permission error",
                "You must be a member for at least 20 days before you can vote in polls."
            )
        )
```