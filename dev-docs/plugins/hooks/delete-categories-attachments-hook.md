# `delete_categories_attachments_hook`

This hook wraps the standard function that Misago uses to delete attachments associated with specified categories.


## Location

This hook can be imported from `misago.attachments.hooks`:

```python
from misago.attachments.hooks import delete_categories_attachments_hook
```


## Filter

```python
def custom_delete_categories_attachments_filter(
    action: DeleteCategoriesAttachmentsHookAction,
    categories: Iterable[Union[Category, int]],
    *,
    request: HttpRequest | None=None,
) -> int:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: DeleteCategoriesAttachmentsHookAction`

A standard function used by Misago to delete attachments associated with specified categories.

See the [action](#action) section for details.


#### `categories: Iterable[Union[Category, int]]`

An iterable of categories or their IDs.


#### `request: HttpRequest | None`

The request object or `None`.


### Return value

An `int` with the number of attachments marked for deletion.


## Action

```python
def delete_categories_attachments_action(
    categories: Iterable[Union[Category, int]],
    *,
    request: HttpRequest | None=None,
) -> int:
    ...
```

A standard function used by Misago to delete attachments associated with specified categories.


### Arguments

#### `categories: Iterable[Union[Category, int]]`

An iterable of categories or their IDs.


#### `request: HttpRequest | None`

The request object or `None`.


### Return value

An `int` with the number of attachments marked for deletion.


## Example

The code below implements a custom filter function that logs delete.

```python
import logging
from typing import Iterable, Protocol, Union

from django.http import HttpRequest
from misago.attachments.hooks import delete_categories_attachments_hook
from misago.categories.models import Category

logger = logging.getLogger("attachments.delete")


@delete_categories_attachments_hook.append_filter
def log_delete_categories_attachments(
    action,
    categories: Iterable[Union[Category, int]],
    *,
    request: HttpRequest | None = None,
) -> int:
    deleted = action(categories, request=request)

    if request and request.user.is_authenticated:
        user = f"#{request.user.id}: {request.user.username}"
    else:
        user = None

    logger.info(
        "Deleted categories attachments: %s",
        str(deleted),
        extra={"user": user},
    )

    return deleted
```