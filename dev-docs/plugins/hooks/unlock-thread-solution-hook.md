# `unlock_thread_solution_hook`

This hook allows plugins to replace or extend the logic used to unlock the thread’s solution.


## Location

This hook can be imported from `misago.solutions.hooks`:

```python
from misago.solutions.hooks import unlock_thread_solution_hook
```


## Filter

```python
def custom_unlock_thread_solution_filter(
    action: UnlockThreadSolutionHookAction,
    thread: Thread,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: UnlockThreadSolutionHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `thread: Thread`

The thread to update.


#### `commit: bool`

Whether the updated thread instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Action

```python
def unlock_thread_solution_action(
    thread: Thread, commit: bool=True, request: HttpRequest | None=None
) -> None:
    ...
```

Misago function used to unlock the thread’s solution.


### Arguments

#### `thread: Thread`

The thread to update.


#### `commit: bool`

Whether the updated thread instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Example

Record the user who unlocked the solution:

```python
from django.http import HttpRequest
from misago.solutions.hooks import unlock_thread_solution_hook
from misago.threads.models import Thread


@unlock_thread_solution_hook.append_filter
def record_unlocked_solution_user(
    action,
    thread: Thread,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> None:
    action(thread, False, request)

    if request:
        thread.plugin_data.update(
            {
                "solution_unlocked_user_id": request.user.id,
                "solution_unlocked_user_ip": request.user_ip,
            }
        )

    if commit:
        thread.save()
```