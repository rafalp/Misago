# `synchronize_category_hook`

This hook allows plugins to replace or extend the logic used to synchronize categories.

Category synchronization updates a category’s thread and post counts, as well as its last thread activity.


## Location

This hook can be imported from `misago.categories.hooks`:

```python
from misago.categories.hooks import synchronize_category_hook
```


## Filter

```python
def custom_synchronize_category_filter(
    action: SynchronizeCategoryHookAction,
    category: Category,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: SynchronizeCategoryHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `category: Category`

The category to synchronize.


#### `commit: bool`

Whether the updated category instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Action

```python
def synchronize_category_action(
    category: Category,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> None:
    ...
```

Misago function for synchronizing a category.


### Arguments

#### `category: Category`

The category to synchronize.


#### `commit: bool`

Whether the updated category instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Example

Record the last user who synchronized the category:

```python
from django.http import HttpRequest
from misago.categories.hooks import synchronize_category_hook
from misago.categories.models import Category


@synchronize_category_hook.append_filter
def record_user_who_synced_category(
    action,
    category: Category,
    commit: bool = True,
    request: HttpRequest | None = None,
):
    if request:
        data.plugin_data["last_synchronized"] = {
            "user_id": request.user.id,
            "user_ip": request.user_ip,
        }
    else:
        data.plugin_data["last_synchronized"] = None

    action(category, commit, request)
```