# `unwatch_thread_hook`

This hook allows plugins to replace or extend the logic used to unwatch a thread for a user.”


## Location

This hook can be imported from `misago.notifications.hooks`:

```python
from misago.notifications.hooks import unwatch_thread_hook
```


## Filter

```python
def custom_unwatch_thread_filter(
    action: UnwatchThreadHookAction,
    thread: Thread,
    user: 'User',
    request: HttpRequest | None=None,
) -> bool:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: UnwatchThreadHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `thread: Thread`

The thread to unwatch.


#### `user: User`

The user who is unwatching the thread.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

`True` if any `WatchedThread` instances were deleted, and `False` if not.


## Action

```python
def unwatch_thread_action(
    thread: Thread, user: 'User', request: HttpRequest | None=None
) -> bool:
    ...
```

Misago function for deleting `WatchedThread` instances associated with a user and a thread.


### Arguments

#### `thread: Thread`

The thread to unwatch.


#### `user: User`

The user who is unwatching the thread.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

`True` if any `WatchedThread` instances were deleted, and `False` if not.


## Example

Record in the database when a user unwatches a thread:

```python
from django.http import HttpRequest
from misago.notifications.hooks import unwatch_thread_hook
from misago.threads.models import Thread
from misago.users.models import User
from myplugin.models import UnwatchedThread


@unwatch_thread_hook.append_filter
def record_unwatched_thread(
    action,
    thread: Thread,
    user: User,
    request: HttpRequest | None = None,
) -> bool:
    deleted = action(thread, user, request)

    if deleted:
        UnwatchedThread.objects.create(thread=thread, user=user)

    return deleted
```