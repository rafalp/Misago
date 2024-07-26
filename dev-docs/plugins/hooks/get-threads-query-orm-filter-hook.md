# `get_threads_query_orm_filter_hook`

This hook wraps the standard function that Misago uses to get Django's `Q` object instance to retrieve threads using a specified query.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import get_threads_query_orm_filter_hook
```


## Filter

```python
def custom_get_threads_query_orm_filter_filter(
    action: GetThreadsQueryORMFilterHookAction,
    query: CategoryThreadsQuery | str,
    categories: list[int],
    user_id: int | None,
) -> Q | None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadsQueryORMFilterHookAction`

A standard Misago function used to get Django's `Q` object instance to retrieve threads using a specified query.

See the [action](#action) section for details.


#### `query: CategoryThreadsQuery | str`

A `CategoryThreadsQuery` `StrEnum` or a `str` with the name of a query to use.


#### `categories: set[int]`

A `set` of `int`s with category IDs.


#### `user_id: int | None`

An `int` with the currently authenticated user ID, or `None` if the user is anonymous.


### Return value

A `Q` object instance to pass to the threads queryset's `filter()`.


## Action

```python
def get_threads_query_orm_filter_action(
    query: CategoryThreadsQuery | str,
    categories: set[int],
    user_id: int | None,
) -> Q | None:
    ...
```

A standard Misago function used to get Django's `Q` object instance to retrieve threads using a specified query.


### Arguments

#### `query: CategoryThreadsQuery | str`

A `CategoryThreadsQuery` `StrEnum` or a `str` with the name of a query to use.


#### `categories: set[int]`

A `set` of `int`s with category IDs.


#### `user_id: int | None`

An `int` with the currently authenticated user ID, or `None` if the user is anonymous.


### Return value

A `Q` object instance to pass to the threads queryset's `filter()`.


## Example

The code below implements a custom filter function that specifies a custom query to use when retrieving the threads list:

```python
from django.db.models import Q
from misago.permissions.hooks import get_threads_query_orm_filter_hook

@get_threads_query_orm_filter_hook.append_filter
def get_category_access_level(
    action,
    query: str,
    categories: set[int],
    user_id: int | None,
) -> Q | None:
    # Show user only their unapproved threads
    if query == "unapproved_only":
        return Q(
            category_id__in=categories,
            starter_id=user_id,
            is_unapproved=True,
        )

    return action(query, categories, user_id)
```