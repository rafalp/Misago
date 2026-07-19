# `set_private_thread_owner_hook`

This hook allows plugins to replace or extend the logic for setting the owner of a private thread.


## Location

This hook can be imported from `misago.privatethreads.hooks`:

```python
from misago.privatethreads.hooks import set_private_thread_owner_hook
```


## Filter

```python
def custom_set_private_thread_owner_filter(
    action: SetPrivateThreadOwnerHookAction,
    thread: Thread,
    new_owner: 'User',
    request: HttpRequest | None=None,
) -> 'bool':
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: SetPrivateThreadOwnerHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `thread: Thread`

The thread whose owner will be set.


#### `new_owner: User`

The user to set as the thread's new owner.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

A `bool`: `True` if the new owner was set, or `False` otherwise.


## Action

```python
def set_private_thread_owner_action(
    thread: Thread, new_owner: 'User', request: HttpRequest | None=None
) -> 'bool':
    ...
```

Misago function for setting the owner of a private thread.


### Arguments

#### `thread: Thread`

The thread whose owner will be set.


#### `new_owner: User`

The user to set as the thread's new owner.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

A `bool`: `True` if the new owner was set, or `False` otherwise.


## Example

Record the user who set the thread owner:

```python
from django.http import HttpRequest
from misago.privatethreads.hooks import set_private_thread_owner_hook
from misago.threads.models import Thread
from misago.users.models import User


@set_private_thread_owner_hook.append_filter
def record_private_thread_owner_set_actor(
    action,
    thread: Thread,
    new_owner: User,
    request: HttpRequest | None = None,
) -> bool:
    set_owner = action(thread, new_owner, request)

    if set_owner and request:
        thread.plugin_data["set_owner"] = {
            "user_id": request.user.id,
            "user_ip": request.user_ip,
        }
        thread.save(update_fields=["plugin_data"])

    return set_owner
```