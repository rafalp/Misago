# `serialize_category_data_hook`

This hook wraps the standard function that Misago uses to create a JSON-serializable `dict` with the category data to populate the `CategoriesProxy` and cache across requests.


## Location

This hook can be imported from `misago.categories.hooks`:

```python
from misago.categories.hooks import serialize_category_data_hook
```


## Filter

```python
def custom_serialize_category_data_filter(
    action: SerializeCategoryDataHookAction, result: dict[str, Any]
) -> dict[str, Any]:
    ...
```

A function implemented by a plugin that can be registered in this hook.


#### `result: dict[str, Any]`

A `dict` with the category data returned by the queryset.


### Return value

A Python `dict` with JSON-serializable category data.


## Action

```python
def serialize_category_data_action(result: dict[str, Any]) -> dict[str, Any]:
    ...
```

Misago function used to create a JSON-serializable `dict` with category data to cache and use to create a `CategoryProxy` instance.


### Arguments

#### `result: dict[str, Any]`

A `dict` with the category data returned by the queryset.


### Return value

A Python `dict` with JSON-serializable category data.


## Example

The code below implements a custom filter function that includes a custom data in `plugin_data`:

```python
from typing import Any
from misago.categories.hooks import serialize_category_data_hook


@serialize_category_data_hook.append_filter
def include_plugin_permission_in_data(action, result: result[str, Any]) -> dict:
    data = action(groups)

    if plugin_flag := result["plugin_data"].get("plugin_flag"):
        data["plugin_data"]["plugin_flag"] = plugin_flag

    return data
```