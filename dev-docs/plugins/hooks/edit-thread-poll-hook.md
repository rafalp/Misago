# `edit_thread_poll_hook`

This hook allows plugins to replace or extend the standard logic for saving an edited poll in the database.


## Location

This hook can be imported from `misago.polls.hooks`:

```python
from misago.polls.hooks import edit_thread_poll_hook
```


## Filter

```python
def custom_edit_thread_poll_filter(
    action: EditThreadPollHookAction,
    thread: Thread,
    poll: Poll,
    user: 'User',
    request: HttpRequest | None,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: EditThreadPollHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `thread: Thread`

The thread instance.


#### `poll: Poll`

The poll instance to save in the database.


#### `user: User`

The user who edited the poll.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Action

```python
def edit_thread_poll_action(
    thread: Thread, poll: Poll, user: 'User', request: HttpRequest | None
) -> None:
    ...
```

Misago function that saves an edited poll.


### Arguments

#### `thread: Thread`

The thread instance.


#### `poll: Poll`

The poll instance to save in the database.


#### `user: User`

The user who edited the poll.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Example

This plugin saves the user who edited the poll in its `plugin_data` field.

```python
from django.http import HttpRequest
from django.utils import timezone
from misago.polls.hooks import edit_thread_poll_hook
from misago.polls.models import Poll
from misago.threads.models import Thread
from misago.users.models import User

@edit_thread_poll_hook.append_filter
def save_poll_edit_data(
    action,
    thread: Thread,
    poll: Poll,
    user: User,
    request: HttpRequest | None,
) -> None:
    poll.plugin_data.set_default("edits", []).append(
        {
            "user_id": user.id,
            "username": user.username,
            "datetime": timezone.now().isoformat(),
        }
    )

    action(thread, poll, user, request)
```