# `serialize_group_plugin_data_hook`

This hook wraps a Misago function that creates a JSON-serializable `dict` containing the group's plugin data. The resulting data is used to populate the `GroupProxy` and is cached across requests.


## Location

This hook can be imported from `misago.users.hooks`:

```python
from misago.users.hooks import serialize_group_plugin_data_hook
```


## Filter

```python
def custom_serialize_group_plugin_data_filter(
    action: SerializeGroupPluginDataHookAction, result: dict[str, Any]
) -> dict[str, Any]:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: SerializeGroupPluginDataHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `result: dict[str, Any]`

A `dict` containing the group data returned by the queryset.


### Return value

A Python `dict` with JSON-serializable plugin data.


## Action

```python
def serialize_group_plugin_data_action(result: dict[str, Any]) -> dict[str, Any]:
    ...
```

Misago function used to create a JSON-serializable `dict` contained the group's plugin data. The result is cached and used to create a `GroupProxy` instance.


### Arguments

#### `result: dict[str, Any]`

A `dict` containing the group data returned by the queryset.


### Return value

A Python `dict` with JSON-serializable plugin data.


## Example

The code below implements a custom filter function that includes custom data in `plugin_data`:

```python
from typing import Any
from misago.users.hooks import serialize_group_plugin_data_hook


@serialize_group_plugin_data_hook.append_filter
def include_plugin_flag_in_data(
    action, result: dict[str, Any]
) -> dict[str, Any]:
    plugin_data = action(result)

    if plugin_flag := result["plugin_data"].get("plugin_flag"):
        plugin_data["plugin_flag"] = plugin_flag

    return plugin_data
```