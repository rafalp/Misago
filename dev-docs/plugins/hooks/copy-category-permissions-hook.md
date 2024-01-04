# `copy_category_permissions_hook`

This hook wraps the standard function that Misago uses to copy category permissions.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import copy_category_permissions_hook
```


## Filter

```python
def custom_copy_category_permissions_filter(
    action: CopyCategoryPermissionsHookAction,
    src: Category,
    dst: Category,
    request: HttpRequest | None=None,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CopyCategoryPermissionsHookAction`

A standard Misago function used to copy permissions from one category to another or the next filter function from another plugin.

See the [action](#action) section for details.


#### `src: Category`

A category to copy permissions from.


#### `dst: Category`

A category to copy permissions to.


#### `request: Optional[HttpRequest]`

The request object or `None` if it was not provided.


## Action

```python
def copy_category_permissions_action(
    src: Category, dst: Category, request: HttpRequest | None=None
) -> None:
    ...
```

A standard Misago function used to copy permissions from one category to another or the next filter function from another plugin.


### Arguments

#### `src: Category`

A category to copy permissions from.


#### `dst: Category`

A category to copy permissions to.


#### `request: Optional[HttpRequest]`

The request object or `None` if it was not provided.


## Example

The code below implements a custom filter function that copies additional models with the plugin's category permissions:

```python
from django.http import HttpRequest
from misago.permissions.hooks import copy_category_permissions_hook
from misago.users.models import Category

from .models PluginCategoryPermissions


@copy_category_permissions_hook.append_filter
def copy_group_plugin_perms(
    action, src: Category, dst: Category, request: HttpRequest | None = None,
) -> None:
    # Delete old permissions
    PluginCategoryPermissions.objects.filter(category=dst).delete()

    # Copy permissions
    for permission in PluginCategoryPermissions.objects.filter(category=src):
        PluginCategoryPermissions.objects.create(
            category=dst,
            group_id=permission.group_id,
            can_do_something=permission.can_do_something,
        )

    # Call the next function in chain
    return action(group, **kwargs)
```