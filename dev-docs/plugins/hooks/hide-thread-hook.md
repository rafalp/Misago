# `hide_thread_hook`

This hook allows plugins to replace or extend the logic used to hide a thread.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import hide_thread_hook
```


## Filter

```python
def custom_hide_thread_filter(
    action: HideThreadHookAction,
    thread: Thread,
    hidden_by: Union['User', str],
    hidden_reason: str | None=None,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> bool:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: HideThreadHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `thread: Thread`

A `Thread` to hide.


#### `hidden_by: User | str`

The user who hid the thread.


#### `hidden_reason: str | None`

A `str` with a short description of why the thread was hidden, or `None`.


#### `commit: bool = True`

Whether the updated thread instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

`True` if the thread was hidden, `False` otherwise.


## Action

```python
def hide_thread_action(
    thread: Thread,
    hidden_by: Union['User', str],
    hidden_reason: str | None=None,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> bool:
    ...
```

Misago function for hiding a thread.


### Arguments

#### `thread: Thread`

A `Thread` to hide.


#### `hidden_by: User | str`

The user who hid the thread.


#### `hidden_reason: str | None`

A `str` with a short description of why the thread was hidden, or `None`.


#### `commit: bool = True`

Whether the updated thread instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

`True` if the thread was hidden, `False` otherwise.


## Example

Register ip of user who hid the thread

```python
from django.http import HttpRequest
from misago.threads.hooks import hide_thread_hook
from misago.threads.models import Thread
from misago.users.models import User


@hide_thread_hook.append_filter
def register_user_that_hid_thread(
    action,
    thread: Thread,
    hidden_by: User | str,
    hidden_reason: str | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    if not action(thread, hidden_by, hidden_reason, commit=False, request=request):
        return False

    if request:
        thread.plugin_data["hidden_by_ip"] = request.user_ip

    if commit:
        thread.save()

    return True