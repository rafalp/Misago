# `get_categories_query_values_hook`

This hook wraps the standard Misago function used to retrieve a set of arguments for the `values` call on the categories queryset.


## Location

This hook can be imported from `misago.categories.hooks`:

```python
from misago.categories.hooks import get_categories_query_values_hook
```


## Filter

```python
def custom_get_categories_query_values_filter(action: GetCategoriesQueryValuesHookAction) -> set[str]:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Return value

A Python `set` with names of the `Category` model fields to include in the queryset.


## Action

```python
def get_categories_query_values_action(self) -> set[str]:
    ...
```

A standard Misago function used to retrieve a set of arguments for the `values` call on the categories queryset.


### Return value

A Python `set` with names of the `Category` model fields to include in the queryset.


## Example

The code below implements a custom filter function that includes the `plugin_data` field in the queryset.

```python
from misago.categories.hooks import get_categories_query_values_hook


@get_categories_query_values_hook.append_filter
def include_plugin_data_in_query(action) -> set[str]:
    fields = action(groups)
    fields.add("plugin_data")
    return fields
```