# `delete_thread_poll_hook`

This hook allows plugins to replace or extend the standard logic for deleting a thread poll.


## Location

This hook can be imported from `misago.polls.hooks`:

```python
from misago.polls.hooks import delete_thread_poll_hook
```


## Filter

```python
def custom_delete_thread_poll_filter(
    action: DeleteThreadPollHookAction,
    thread: Thread,
    poll: Poll,
    user: 'User',
    request: HttpRequest | None,
) -> ThreadUpdate:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: DeleteThreadPollHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `thread: Thread`

The thread to update.


#### `poll: Poll`

The poll to delete.


#### `user: User`

The user who deleted the poll, recorded as the actor of the thread update.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

A `ThreadUpdate` instance.


## Action

```python
def delete_thread_poll_action(
    thread: Thread, poll: Poll, user: 'User', request: HttpRequest | None
) -> ThreadUpdate:
    ...
```

Misago function that deletes a thread's poll, updates the thread instance, and creates a new thread update object.


### Arguments

#### `thread: Thread`

The thread to update.


#### `poll: Poll`

The poll to delete.


#### `user: User`

The user who deleted the poll, recorded as the actor of the thread update.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

A `ThreadUpdate` instance.


## Example

This plugin automatically hides newly created thread update if deleted poll existed for less than 15 minutes.

```python
from django.http import HttpRequest
from django.utils import timezone
from misago.polls.hooks import delete_thread_poll_hook
from misago.polls.models import Poll
from misago.threads.models import Thread
from misago.threadupdates.hide import hide_thread_update
from misago.threadupdates.models import ThreadUpdate
from misago.users.models import User

@delete_thread_poll_hook.append_filter
def delete_plugin_relations(
    action,
    thread: Thread,
    poll: Poll,
    user: User,
    request: HttpRequest | None,
) -> ThreadUpdate:
    # Run standard deletion logic
    thread_update = action(thread, poll, user, request)

    poll_age = timezone.now() - poll.started_at
    if poll_age.total_seconds() < 900:
        hide_thread_update(thread_update, request)

    return thread_update
```