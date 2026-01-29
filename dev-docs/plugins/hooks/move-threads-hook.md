# `move_threads_hook`

This hook allows plugins to replace or extend the logic used to move threads to a new category.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import move_threads_hook
```


## Filter

```python
def custom_move_threads_filter(
    action: MoveThreadsHookAction,
    threads: Iterable[Thread],
    new_category: Category,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: MoveThreadsHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `threads: Iterable[Thread]`

The iterable of threads to move.


#### `new_category: category`

A `Category` to move threads to.


#### `commit: bool`

Whether the threads' `category` field should be updated directly in the database using `QuerySet.update()`.

When True, only the category column is saved. If other fields need updating, set this to False and handle updates manually.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Action

```python
def move_threads_action(
    threads: Iterable[Thread],
    new_category: Category,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> None:
    ...
```

Misago function for moving threads to a new category.


### Arguments

#### `threads: Iterable[Thread]`

The iterable of threads to move.


#### `new_category: category`

A `Category` to move threads to.


#### `commit: bool`

Whether the threads' `category` field should be updated directly in the database using `QuerySet.update()`.

When True, only the category column is saved. If other fields need updating, set this to False and handle updates manually.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Example

Update `category` attribute on plugin model:

```python
from typing import Iterable

from django.http import HttpRequest
from misago.categories.models import Category
from misago.threads.hooks import move_threads_hook
from misago.threads.models import Thread

from .models import PluginModel


@move_threads_hook.append_filter
def move_plugin_models_to_new_category(
    action,
    threads: Iterable[Thread],
    new_category: Category,
    commit: bool = True,
    request: HttpRequest | None = None,
):
    action(thread, data, commit, request)

    PluginModel.objects.filter(
        thread__in=threads
    ).update(category=new_category)