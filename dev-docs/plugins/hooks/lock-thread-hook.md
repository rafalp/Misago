# `lock_thread_hook`

This hook allows plugins to replace or extend the logic used to lock a thread.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import lock_thread_hook
```


## Filter

```python
def custom_lock_thread_filter(
    action: LockThreadHookAction,
    thread: Thread,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> bool:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: LockThreadHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `thread: Thread`

A `Thread` to lock.


#### `commit: bool = True`

Whether the updated thread instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

`True` if the thread was locked, `False` otherwise.


## Action

```python
def lock_thread_action(
    thread: Thread, commit: bool=True, request: HttpRequest | None=None
) -> bool:
    ...
```

Misago function for locking a thread.


### Arguments

#### `thread: Thread`

A `Thread` to lock.


#### `commit: bool = True`

Whether the updated thread instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

`True` if the thread was locked, `False` otherwise.


## Example

Register user who locked the thread.

```python
from django.http import HttpRequest
from misago.threads.hooks import lock_thread_hook
from misago.threads.models import Thread


@lock_thread_hook.append_filter
def register_user_that_locked_thread(
    action,
    thread: Thread,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    if not action(thread, commit=False, request=request):
        return False

    if request:
        thread.plugin_data["locked_by"] = request.user.id

    if commit:
        thread.save()

    return True