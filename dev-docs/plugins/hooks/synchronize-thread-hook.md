# `synchronize_thread_hook`

This hook allows plugins to replace or extend the logic used to synchronize threads.

Thread synchronization updates a thread’s reply count, the IDs and timestamps of the first and last posts, the attributes of the first and last posters, and status flags such as has_unapproved_posts.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import synchronize_thread_hook
```


## Filter

```python
def custom_synchronize_thread_filter(
    action: SynchronizeThreadHookAction,
    thread: Thread,
    data: dict,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: SynchronizeThreadHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `thread: Thread`

The thread to synchronize.


#### `data: dict`

A `dict` of new attributes to set on the thread.


#### `commit: bool`

Whether the updated thread instance should be saved to the database.

Defaults to True.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Action

```python
def synchronize_thread_action(
    thread: Thread,
    data: dict,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> None:
    ...
```

Misago function for synchronizing a thread.


### Arguments

#### `thread: Thread`

The thread to synchronize.


#### `data: dict`

A `dict` of new attributes to set on the thread.


#### `commit: bool`

Whether the updated thread instance should be saved to the database.

Defaults to True.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Example

Record the IP address used to change the thread owner:

```python
from django.http import HttpRequest
from misago.privatethreadmembers.hooks import synchronize_thread_hook
from misago.threads.models import Thread
from misago.threadupdates.models import ThreadUpdate
from misago.users.models import User


@synchronize_thread_hook.append_filter
def record_private_thread_owner_change_actor_ip(
    action,
    actor: User | str | None,
    thread: Thread,
    new_owner: User,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    thread_update = action(actor, thread, new_owner, request)

    thread_update.plugin_data["user_ip"] = request.user_ip
    thread_update.save(update_fields=["plugin_data"])

    return thread_update
```