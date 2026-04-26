# `unlock_thread_hook`

This hook allows plugins to replace or extend the logic used to unlock a thread.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import unlock_thread_hook
```


## Filter

```python
def custom_unlock_thread_filter(
    action: UnlockThreadHookAction,
    thread: Thread,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> bool:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: UnlockThreadHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `thread: Thread`

A `Thread` to unlock.


#### `commit: bool = True`

Whether the updated thread instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

`True` if the thread was unlocked, `False` otherwise.


## Action

```python
def unlock_thread_action(
    thread: Thread, commit: bool=True, request: HttpRequest | None=None
) -> bool:
    ...
```

Misago function for unlocking a thread.


### Arguments

#### `thread: Thread`

A `Thread` to unlock.


#### `commit: bool = True`

Whether the updated thread instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

`True` if the thread was unlocked, `False` otherwise.


## Example

Register information about user who unlocked the thread

```python
from django.http import HttpRequest
from misago.threads.hooks import unlock_thread_hook
from misago.threads.models import Thread


@unlock_thread_hook.append_filter
def register_user_that_unlocked_thread(
    action,
    thread: Thread,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    if not action(thread, commit=False, request=request):
        return False

    if request:
        thread.plugin_data["unlocked_by"] = request.user.id

    if commit:
        thread.save()

    return True