# `change_private_thread_owner_hook`

This hook allows plugins to replace or extend the logic for changing a private thread owner.


## Location

This hook can be imported from `misago.privatethreads.hooks`:

```python
from misago.privatethreads.hooks import change_private_thread_owner_hook
```


## Filter

```python
def custom_change_private_thread_owner_filter(
    action: ChangePrivateThreadOwnerHookAction,
    actor: Union['User', str, None],
    thread: Thread,
    new_owner: 'User',
    request: HttpRequest | None=None,
) -> 'ThreadUpdate':
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: ChangePrivateThreadOwnerHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `actor: User | str | None`

The actor performing the action: either a `User` instance, a `str` with a name, or `None` if not available.


#### `thread: Thread`

The thread whose owner is being changed.


#### `new_owner: User`

The user who will become the new owner of the thread.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

A `ThreadUpdate` instance.


## Action

```python
def change_private_thread_owner_action(
    actor: Union['User', str, None],
    thread: Thread,
    new_owner: 'User',
    request: HttpRequest | None=None,
) -> 'ThreadUpdate':
    ...
```

Misago function for changing a private thread's owner.


### Arguments

#### `actor: User | str | None`

The actor performing the action: either a `User` instance, a `str` with a name, or `None` if not available.


#### `thread: Thread`

The thread whose owner is being changed.


#### `new_owner: User`

The user who will become the new owner of the thread.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

A `ThreadUpdate` instance.


## Example

Record the IP address used to change the thread owner:

```python
from django.http import HttpRequest
from misago.privatethreads.hooks import change_private_thread_owner_hook
from misago.threads.models import Thread
from misago.threadupdates.models import ThreadUpdate
from misago.users.models import User


@change_private_thread_owner_hook.append_filter
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