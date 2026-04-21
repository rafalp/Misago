# `select_thread_solution_hook`

This hook allows plugins to replace or extend the logic used to selecting a post as the thread’s solution.


## Location

This hook can be imported from `misago.solutions.hooks`:

```python
from misago.solutions.hooks import select_thread_solution_hook
```


## Filter

```python
def custom_select_thread_solution_filter(
    action: SelectThreadSolutionHookAction,
    thread: Thread,
    post: Post,
    user: Union['User', str],
    commit: bool=True,
    request: HttpRequest | None=None,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: SelectThreadSolutionHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `thread: Thread`

The thread to update.


#### `post: Post`

The post to set as the solution.


#### `user: User | str`

The user who selected the solution.


#### `commit: bool = True`

Whether the updated thread instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Action

```python
def select_thread_solution_action(
    thread: Thread,
    post: Post,
    user: Union['User', str],
    commit: bool=True,
    request: HttpRequest | None=None,
) -> None:
    ...
```

Misago function for selecting a post as the thread’s solution.


### Arguments

#### `thread: Thread`

The thread to update.


#### `post: Post`

The post to set as the solution.


#### `user: User | str`

The user who selected the solution.


#### `commit: bool = True`

Whether the updated thread instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Example

Record the IP address of the user who selected the solution:

```python
from django.http import HttpRequest
from misago.solutions.hooks import select_thread_solution_hook
from misago.threads.models import Thread, Post
from misago.users.models import User


@select_thread_solution_hook.append_filter
def record_solution_user_ip_address(
    action,
    thread: Thread,
    post: Post,
    user: User | str,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> None:
    action(thread, post, user, False, request)

    if request:
        thread.plugin_data["solution_user_ip"] = request.user_ip

    if commit:
        thread.save()
```