# `pin_thread_in_category_hook`

This hook allows plugins to replace or extend the logic used to pin a thread in a category.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import pin_thread_in_category_hook
```


## Filter

```python
def custom_pin_thread_in_category_filter(
    action: PinThreadInCategoryHookAction,
    thread: Thread,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> bool:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: PinThreadInCategoryHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `thread: Thread`

A `Thread` to pin in a category.


#### `commit: bool = True`

Whether the updated thread instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

`True` if the thread was pinned, `False` otherwise.


## Action

```python
def pin_thread_in_category_action(
    thread: Thread, commit: bool=True, request: HttpRequest | None=None
) -> bool:
    ...
```

Misago function for pinning a thread in a category.


### Arguments

#### `thread: Thread`

A `Thread` to pin in a category.


#### `commit: bool = True`

Whether the updated thread instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

`True` if the thread was pinned, `False` otherwise.


## Example

Register user who pinned the thread.

```python
from django.http import HttpRequest
from misago.threads.hooks import pin_thread_in_category_hook
from misago.threads.models import Thread


@pin_thread_in_category_hook.append_filter
def register_user_that_pinned_thread_in_category(
    action,
    thread: Thread,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    if not action(thread, commit=False, request=request):
        return False

    if request:
        thread.plugin_data["pinned_in_category_by"] = request.user.id

    if commit:
        thread.save()

    return True