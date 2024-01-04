# `build_user_category_permissions_hook`

This hook wraps the standard function that Misago uses to build user category permissions.

Category permissions are stored as a Python `dict` with permission names as keys and values being category IDs with the associated permission:

```python
category_permissions = {
    "see": [1, 2, 3],
    "browse": [1, 2, 3],
    "start": [1, 2],
    "reply": [1, 2, 3],
    "attachments": [1, 2, 3],
}
```

Plugins can add custom permissions to this dict.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import build_user_category_permissions_hook
```


## Filter

```python
def custom_build_user_category_permissions_filter(
    action: BuildUserCategoryPermissionsHookAction,
    groups: list[Group],
    categories: dict[int, Category],
    category_permissions: dict[int, list[str]],
    user_permissions: dict,
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: BuildUserCategoryPermissionsHookAction`

A standard Misago function used to build user category permissions or the next filter function from another plugin.

See the [action](#action) section for details.


#### `groups: list[Group]`

A list of groups user belongs to.


#### `categories: dict[int, Category]`

A `dict` of categories.


#### `category_permissions: dict[int, list[str]]`

A Python `dict` containing lists of category permissions read from the database, indexed by category IDs.


#### `user_permissions: dict`

A Python `dict` with user permissions build so far.


### Return value

A Python `dict` with category permissions.


## Action

```python
def build_user_category_permissions_action(
    groups: list[Group],
    categories: dict[int, Category],
    category_permissions: dict[int, list[str]],
    user_permissions: dict,
) -> dict:
    ...
```

A standard Misago function used to get user category permissions.


### Arguments

#### `groups: list[Group]`

A list of groups user belongs to.


#### `categories: dict[int, Category]`

A `dict` of categories.


#### `category_permissions: dict[int, list[str]]`

A Python `dict` containing lists of category permissions read from the database, indexed by category IDs.


#### `user_permissions: dict`

A Python `dict` with user permissions build so far.


### Return value

A Python `dict` with category permissions.


## Example

The code below implements a custom filter function that includes a custom permission in user's category permissions, if they can browse it:

```python
from misago.categories.models import Category
from misago.permissions.enums import CategoryPermission
from misago.permissions.hooks import build_user_category_permissions_hook
from misago.users.models import Group


@build_user_category_permissions_hook.append_filter
def include_plugin_permission(
    action,
    groups: list[Group],
    categories: dict[int, Category],
    category_permissions: dict[int, list[str]],
    user_permissions: dict,
) -> dict:
    permissions = action(group, categories, category_permissions, user_permissions)
    permissions["plugin"] = []

    for category_id in categories:
        if (
            category_id in permissions[CategoryPermission.BROWSE]
            and "plugin" in category_permissions.get(category_id, [])
        ):
            permissions["plugin"].append(category_id)

    return permissions
```