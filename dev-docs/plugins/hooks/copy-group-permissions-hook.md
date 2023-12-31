# `copy_group_permissions_hook`

This hook wraps the standard function that Misago uses to copy group permissions.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import copy_group_permissions_hook
```


## Filter

```python
def custom_copy_group_permissions_filter(
    action: CopyGroupPermissionsHookAction,
    src: Group,
    dst: Group,
    request: HttpRequest | None=None,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CopyGroupPermissionsHookAction`

A standard Misago function used to copy permissions from one user group to another or the next filter function from another plugin.

See the [action](#action) section for details.


#### `src: Group`

A group to copy permissions from.


#### `dst: Group`

A group to copy permissions to.


#### `request: Optional[HttpRequest]`

The request object or `None` if it was not provided.


## Action

```python
def copy_group_permissions_action(
    src: Group, dst: Group, request: HttpRequest | None=None
) -> None:
    ...
```

A standard Misago function used to copy permissions from one user group to another or the next filter function from another plugin.


### Arguments

#### `src: Group`

A group to copy permissions from.


#### `dst: Group`

A group to copy permissions to.


#### `request: Optional[HttpRequest]`

The request object or `None` if it was not provided.


## Example

The code below implements a custom filter function that copies a permission from one group's `plugin_data` to the other:

```python
from django.http import HttpRequest
from misago.permissions.hooks import copy_group_permissions_hook
from misago.users.models import Group


@copy_group_permissions_hook.append_filter
def copy_group_plugin_perms(
    action, src: Group, dst: Group, request: HttpRequest | None = None,
) -> None:
    dst.plugin_data["can_do_plugin_thing"] = src.plugin_data["can_do_plugin_thing"]

    # Call the next function in chain
    return action(group, **kwargs)
```