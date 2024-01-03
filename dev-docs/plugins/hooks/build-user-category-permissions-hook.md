# `build_user_category_permissions_hook`

This hook wraps the standard function that Misago uses to get user permissions.

User permissions are a Python `dict`. This `dict` is first retrieved from the cache, and if that fails, a new `dict` is built from the user's groups.

Plugins can use this hook to make additional changes to the final Python `dict` based on user data.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import build_user_category_permissions_hook
```


## Filter

```python
def custom_build_user_category_permissions_filter(
    action: BuildUserCategoryPermissionsHookAction,
    user: User,
    cache_versions: dict,
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: BuildUserCategoryPermissionsHookAction`

A standard Misago function used to get user permissions or the next filter function from another plugin.

See the [action](#action) section for details.


#### `groups: list[Group]`

A list of groups user belongs to.


### Return value

A Python `dict` with user permissions build from their groups.


## Action

```python
def build_user_category_permissions_action(user: User, cache_versions: dict) -> dict:
    ...
```

A standard Misago function used to get user permissions.

Retrieves permissions data from cache or builds new ones.


### Arguments

#### `user: User`

A user to return permissions for.


#### `cache_versions: dict`

A Python `dict` with cache versions.


### Return value

A Python `dict` with user permissions.


## Example

The code below implements a custom filter function that includes a custom permission into the final user permissions, retrieved from their `plugin_data` attribute:

```python
from misago.permissions.hooks import build_user_permissions_hook
from misago.users.models import User


@get_user_permissions_hook.append_filter
def include_plugin_permission(
    action, user: User, cache_versions: dict
) -> dict:
    permissions = action(user, cache_versions)
    permissions["plugin_permission"] = False

    if user.plugin_data.get("plugin_permission"):
        permissions["plugin_permission"] = True

    return permissions
```