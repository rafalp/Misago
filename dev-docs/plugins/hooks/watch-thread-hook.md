# `watch_thread_hook`

This hook allows plugins to replace or extend the logic used to create watched thread objects.


## Location

This hook can be imported from `misago.notifications.hooks`:

```python
from misago.notifications.hooks import watch_thread_hook
```


## Filter

```python
def custom_watch_thread_filter(
    action: WatchThreadHookAction,
    thread: Thread,
    user: 'User',
    send_emails: bool=True,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> WatchedThread:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: WatchThreadHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `thread: Thread`

The thread to watch.


#### `user: User`

The user who is watching the thread.


#### `send_emails: bool`

Whether e-mail notifications should be enabled.

Defaults to `True`,


#### `commit: bool`

Whether the new `WatchedThread` instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

New `WatchedThread` instance.


## Action

```python
def watch_thread_action(
    thread: Thread,
    user: 'User',
    send_emails: bool=True,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> WatchedThread:
    ...
```

Misago function for creating a new `WatchedThread` instance.


### Arguments

#### `thread: Thread`

The thread to watch.


#### `user: User`

The user who is watching the thread.


#### `send_emails: bool`

Whether e-mail notifications should be enabled.

Defaults to `True`,


#### `commit: bool`

Whether the new `WatchedThread` instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

New `WatchedThread` instance.


## Example

Record the IP address used to watch the thread:

```python
from django.http import HttpRequest
from misago.notifications.hooks import watch_thread_hook
from misago.notifications.models import WatchedThread
from misago.threads.models import Thread
from misago.users.models import User


@watch_thread_hook.append_filter
def record_watched_thread_user_ip(
    action,
    thread: Thread,
    user: User,
    send_emails: bool = True,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> WatchedThread:
    watched_thread = action(thread, user, send_emails, False, request)

    watched_thread.plugin_data["user_id"] = request.user_ip

    if commit:
        watched_thread.save()

    return watched_thread
```