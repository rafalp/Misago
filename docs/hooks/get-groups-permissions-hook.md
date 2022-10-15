# `get_groups_permissions_hook`

```python
from misago.permissions.hooks import get_groups_permissions_hook

get_groups_permissions_hook.call_action(
    action: GetUserPermissionsAction,
    context: Context,
    data: dict,
    groups_permissions: dict,
    *,
    anonymous: bool = False,
)
```

A filter for the function used by Misago to build permissions from given user groups.

Mutates `groups_permissions` dict using data from `data` dict and other arguments.


## Required arguments

### `action`

```python
async def get_groups_permissions(
    context: Context,
    data: dict,
    groups_permissions: dict,
    *,
    anonymous: bool = False,
) -> dict:
    ...
```

Next filter or built-in function used to builds permissions for given user groups.


### `context`

```python
Context
```

A dict with GraphQL query context.


### `data`

```python
class TypedDict:
    groups: Iterable[UserGroup]
    groups_ids: List[int]
    categories: List[Category]
    moderated_categories: List[int]
```

Mutable dict containing data to use for building final permissions for groups.

Contains at least following keys:

- `groups`: Iterable with `UserGroup` objects for which permissions should be build.
- `groups_ids`: List of ids of given user groups.
- `categories`: List of existing categories.
- `moderated_categories`: List of ids of categories for whose specified groups are moderators.
