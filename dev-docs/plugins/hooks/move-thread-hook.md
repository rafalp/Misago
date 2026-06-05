# `move_thread_hook`

This hook allows plugins to replace or extend the logic used to move a thread to a new category.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import move_thread_hook
```


## Filter

```python
def custom_move_thread_filter(
    action: MoveThreadHookAction,
    thread: Thread,
    new_category: Category,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> bool:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: MoveThreadHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `thread: Thread`

A `Thread` to move.


#### `new_category: Category`

The `Category` to move the thread to.


#### `commit: bool = True`

Whether the updated thread instance should be saved to the database.

Defaults to `True`.

The thread's related objects are always updated, even if this option is set to `False`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

`True` if the thread was moved, `False` otherwise.


## Action

```python
def move_thread_action(
    thread: Thread,
    new_category: Category,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> bool:
    ...
```

Misago function for moving a thread to a new category.


### Arguments

#### `thread: Thread`

A `Thread` to move.


#### `new_category: Category`

The `Category` to move the thread to.


#### `commit: bool = True`

Whether the updated thread instance should be saved to the database.

Defaults to `True`.

The thread's related objects are always updated, even if this option is set to `False`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

`True` if the thread was moved, `False` otherwise.


## Example

Move plugin models associated with the thread along with it:

```python
from django.http import HttpRequest
from misago.categories.models import Category
from misago.threads.hooks import move_thread_hook
from misago.threads.models import Thread

from .models import PluginModel


@move_thread_hook.append_filter
def move_plugin_models_to_new_category(
    action,
    thread: Thread,
    new_category: Category,
    commit: bool = True,
    request: HttpRequest | None = None,
):
    if not action(thread, new_category, commit, request):
        return False

    PluginModel.objects.filter(
        thread=thread
    ).update(category=new_category)

    return True