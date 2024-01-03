# `build_user_permissions_hook`

This hook wraps the standard function that Misago uses to build user permissions from their groups.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import build_user_permissions_hook
```


## Filter

```python
def custom_build_user_permissions_filter(
    action: BuildUserPermissionsHookAction, groups: list[Group]
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: BuildUserPermissionsHookAction`

A standard Misago function used to build user permissions from their groups or the next filter function from another plugin.

See the [action](#action) section for details.


#### `groups: list[Group]`

A list of groups user belongs to.


### Return value

A Python `dict` with user permissions build from their groups.


## Action

```python
def build_user_permissions_action(groups: list[Group]) -> dict:
    ...
```

A standard Misago function used to build user permissions from their groups.


### Arguments

#### `groups: list[Group]`

A list of groups user belongs to.


### Return value

A Python `dict` with user permissions build from their groups.


## Example

The code below implements a custom filter function that includes a custom permission in user permissions:

```python
from misago.permissions.hooks import build_user_permissions_hook
from misago.users.models import Group


@build_user_permissions_hook.append_filter
def include_plugin_permission(
    action, groups: list[Group]
) -> dict:
    permissions = action(groups)
    permissions["plugin_permission"] = False

    for group in groups:
        if group.plugin_data.get("plugin_permission"):
            permissions["plugin_permission"] = True

    return permissions
```