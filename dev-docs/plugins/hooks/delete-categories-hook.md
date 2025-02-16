# `delete_categories_hook`

This hook wraps the standard function that Misago uses to delete category and its children.


## Location

This hook can be imported from `misago.categories.hooks`:

```python
from misago.categories.hooks import delete_categories_hook
```


## Filter

```python
def custom_delete_categories_filter(
    action: DeleteCategoriesHookAction,
    categories: list[Category],
    *,
    move_children_to: Category | bool | None=True,
    move_contents_to: Category | None=None,
    request: HttpRequest | None=None,
) -> int:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: DeleteCategoriesHookAction`

A standard function used by Misago to delete category and its children.


#### `categories: list[Category]`

A list of categories that will be deleted. If `move_children_to` is `None`, it will contain both the deleted category and all its descendants that will also be deleted. Otherwise, `categories` list will contain only single item.


#### `move_children_to: Category | bool | None = True`

A category to move categories children to, `True` to make them root categories, or `None` to delete them too.


#### `move_contents_to: Category | None = None`

A category to move categories content to, or `None` to delete contents too.


#### `request: HttpRequest | None`

The request object or `None`.


## Action

```python
def delete_categories_action(
    categories: list[Category],
    *,
    move_children_to: Category | bool | None=True,
    move_contents_to: Category | None=None,
    request: HttpRequest | None=None,
):
    ...
```

A standard function used by Misago to delete category and its children.


### Arguments

#### `categories: list[Category]`

A list of categories that will be deleted. If `move_children_to` is `None`, it will contain both the deleted category and all its descendants that will also be deleted. Otherwise, `categories` list will contain only single item.


#### `move_children_to: Category | bool | None = True`

A category to move children categories to, `True` to make them root categories, or `None` to delete them too.


#### `move_contents_to: Category | None = None`

A category to move categories content to, or `None` to delete contents too.


#### `request: HttpRequest | None`

The request object or `None`.


## Example

The code below implements a custom filter function that logs delete.

```python
import logging
from typing import list, Protocol

from django.http import HttpRequest
from misago.categories.hooks import delete_categories_hook
from misago.categories.models import Category

logger = logging.getLogger("attachments.delete")


@delete_categories_hook.append_filter
def log_delete_categories(
    action,
    categories: list[Category],
    *,
    move_children_to: Category | bool | None = True,
    move_contents_to: Category | None = None,
    request: HttpRequest | None = None,
):
    action(
        categories,
        move_children_to=move_children_to,
        move_contents_to=move_contents_to,
        request=request,
    )

    if request and request.user.is_authenticated:
        user = f"#{request.user.id}: {request.user.username}"
    else:
        user = None

    logger.info(
        "Deleted categories: %s",
        ", ".join(f"#{c.id}: {c.name}" for c in categories),
        extra={"user": user},
    )
```