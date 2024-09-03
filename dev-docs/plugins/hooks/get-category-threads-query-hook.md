# `get_category_threads_query_hook`

This hook wraps the standard function that Misago uses to get the name of the predefined database `WHERE` clause (represented as a `Q` object instance) to use to retrieve threads from the given category.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import get_category_threads_query_hook
```


## Filter

```python
def custom_get_category_threads_query_filter(
    action: GetCategoryThreadsQueryHookAction,
    permissions: 'UserPermissionsProxy',
    category: dict,
) -> str | list[str] | None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetCategoryThreadsQueryHookAction`

A standard Misago function used to get the name of the predefined database `WHERE` clause (represented as a `Q` object instance) to use to retrieve threads from the given category.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: dict`

A `dict` with category data.


### Return value

A `CategoryThreadsQuery` member or a `str` with a custom clause name. If `None`, the query retrieving threads will skip this category. If multiple clauses should be `OR`ed together, a list of strings or `CategoryThreadsQuery` members can be returned.


## Action

```python
def get_category_threads_query_action(
    permissions: 'UserPermissionsProxy', category: dict
) -> str | list[str] | None:
    ...
```

A standard Misago function used to get the name of the predefined database `WHERE` clause (represented as a `Q` object instance) to use to retrieve threads from the given category.

Standard `WHERE` clauses implemented by Misago can be retrieved from the `CategoryThreadsQuery` `StrEnum`:

```python
from misago.permissions.enums import CategoryThreadsQuery
```


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: dict`

A `dict` with category data.


### Return value

A `CategoryThreadsQuery` member or a `str` with a custom clause name. If `None`, the query retrieving threads will skip this category. If multiple clauses should be `OR`ed together, a list of strings or `CategoryThreadsQuery` members can be returned.


## Example

The code below implements a custom filter function that specifies a custom `WHERE` clause supported by the `get_threads_query_orm_filter_hook`.

```python
from misago.permissions.hooks import get_category_threads_query_hook
from misago.permissions.proxy import UserPermissionsProxy

@get_category_threads_query_hook.append_filter
def get_category_threads_query(
    action,
    permissions: UserPermissionsProxy,
    category: dict,
) -> str | list[str] | None:
    if (
        category.get("plugin_flag") and context == CategoryQueryContext.CURRENT
    ):
        return "plugin-where"

    return action(permissions, category)
```