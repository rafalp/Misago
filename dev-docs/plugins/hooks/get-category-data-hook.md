# `get_category_data_hook`

This hook wraps the standard function that Misago uses to build a `dict` with category data from queryset's result.


## Location

This hook can be imported from `misago.categories.hooks`:

```python
from misago.categories.hooks import get_category_data_hook
```


## Filter

```python
def custom_get_category_data_filter(
    action: GetCategoryDataHookAction, result: dict[str, Any]
) -> dict[str, Any]:
    ...
```

A function implemented by a plugin that can be registered in this hook.


#### `result: dict[str, Any]`

A `dict` with category data returned by the queryset.


### Return value

A Python `dict` with category data to cache and use by Misago.


## Action

```python
def get_category_data_action(result: dict[str, Any]) -> dict[str, Any]:
    ...
```

A standard Misago function used to build a `dict` with category result from queryset's result.


### Arguments

#### `result: dict[str, Any]`

A `dict` with category data returned by the queryset.


### Return value

A Python `dict` with category data to cache and use by Misago.


## Example

The code below implements a custom filter function that includes a custom dict entry using `plugin_data`:

```python
from typing import Any
from misago.categories.hooks import get_category_data_hook


@get_category_data_hook.append_filter
def include_plugin_permission_in_data(action, result: result[str, Any]) -> dict:
    data = action(groups)
    if result.get("plugin_data"):
        data["plugin_flag"] = result["plugin_data"].get("plugin_flag")

    return data
```