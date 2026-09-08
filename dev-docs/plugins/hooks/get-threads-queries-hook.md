# `get_threads_queries_hook`

This hook wraps the standard function that Misago uses to get the names of predefined database `WHERE` clauses, represented as `Q` object instances, for use by other functions to retrieve threads from given categories.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import get_threads_queries_hook
```


## Filter

```python
def custom_get_threads_queries_filter(
    action: GetThreadsQueriesHookAction,
    permissions: 'UserPermissionsProxy',
    category: Union['Category', 'CategoryProxy'],
) -> dict[int, set[str]]:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadsQueriesHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `categories: list[Category | CategoryProxy]`

A list of `Category` and `CategoryProxy` instances.


### Return value

A dict of sets of `CategoryThreadsQuery` members grouped by category id. When set contains more than one `CategoryThreadsQuery`, resulting `Q` expressions should be `OR` together.


## Action

```python
def get_threads_queries_action(
    permissions: 'UserPermissionsProxy',
    category: Union['Category', 'CategoryProxy'],
) -> dict[int, set[str]]:
    ...
```

Standard Misago function used to get the names of predefined database `WHERE` clauses (represented as `Q` object instances) to use by other functions to retrieve threads from given categories.

Standard `WHERE` clauses implemented by Misago can be retrieved from the `CategoryThreadsQuery` `StrEnum`:

```python
from misago.permissions.enums import CategoryThreadsQuery
```


### Arguments

#### `permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `categories: list[Category | CategoryProxy]`

A list of `Category` and `CategoryProxy` instances.


### Return value

A dict of sets of `CategoryThreadsQuery` members grouped by category id. When set contains more than one `CategoryThreadsQuery`, resulting `Q` expressions should be `OR` together.


## Example

The code below implements a custom filter function that removes a category from the queries if its muted by user

```python
from misago.categories.models import Category
from misago.categories.proxy import CategoryProxy
from misago.permissions.hooks import get_threads_queries_hook
from misago.permissions.proxy import UserPermissionsProxy

@get_threads_queries_hook.append_filter
def get_threads_queries(
    action,
    permissions: UserPermissionsProxy,
    categories: list[Category | CategoryProxy],
) -> dict[int, set[str]]:
    queries = action(permissions, categories)

    if permissions.user.is_authenticated:
        muted_categories = permissions.user.plugin_data.get("muted_categories", [])
        for category_id in muted_categories:
            queries.pop(category_id)

    return queries
```