# `clear_thread_solution_hook`

This hook allows plugins to replace or extend the logic used to clear the thread’s solution.


## Location

This hook can be imported from `misago.solutions.hooks`:

```python
from misago.solutions.hooks import clear_thread_solution_hook
```


## Filter

```python
def custom_clear_thread_solution_filter(
    action: ClearThreadSolutionHookAction,
    thread: Thread,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: ClearThreadSolutionHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `thread: Thread`

The thread to update.


#### `commit: bool = True`

Whether the updated thread instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Action

```python
def clear_thread_solution_action(
    thread: Thread, commit: bool=True, request: HttpRequest | None=None
) -> None:
    ...
```

Misago function used to clear the thread’s solution.


### Arguments

#### `thread: Thread`

The thread to update.


#### `commit: bool = True`

Whether the updated thread instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Example

Record the user who cleared the solution:

```python
from django.http import HttpRequest
from misago.solutions.hooks import clear_thread_solution_hook
from misago.threads.models import Thread


@clear_thread_solution_hook.append_filter
def record_cleared_solution_user(
    action,
    thread: Thread,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> None:
    action(thread, False, request)

    if request:
        thread.plugin_data.update(
            {
                "solution_cleared_user_id": request.user.id,
                "solution_cleared_user_ip": request.user_ip,
            }
        )

    if commit:
        thread.save()
```