from typing import Any, Protocol

from ...plugins.hooks import FilterHook


class SerializeGroupPluginDataHookAction(Protocol):
    """
    Misago function used to create a JSON-serializable `dict` contained the
    group's plugin data. The result is cached and used to create a `GroupProxy`
    instance.

    # Arguments

    ## `result: dict[str, Any]`

    A `dict` containing the group data returned by the queryset.

    # Return value

    A Python `dict` with JSON-serializable plugin data.
    """

    def __call__(self, result: dict[str, Any]) -> dict[str, Any]: ...


class SerializeGroupPluginDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: SerializeGroupPluginDataHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `result: dict[str, Any]`

    A `dict` containing the group data returned by the queryset.

    # Return value

    A Python `dict` with JSON-serializable plugin data.
    """

    def __call__(
        self, action: SerializeGroupPluginDataHookAction, result: dict[str, Any]
    ) -> dict[str, Any]: ...


class SerializeGroupPluginDataHook(
    FilterHook[SerializeGroupPluginDataHookAction, SerializeGroupPluginDataHookFilter]
):
    """
    This hook wraps a Misago function that creates a JSON-serializable `dict`
    containing the group's plugin data. The resulting data is used to populate
    the `GroupProxy` and is cached across requests.

    # Example

    The code below implements a custom filter function that includes custom
    data in `plugin_data`:

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
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self, action: SerializeGroupPluginDataHookAction, result: dict[str, Any]
    ) -> dict[str, Any]:
        return super().__call__(action, result)


serialize_group_plugin_data_hook = SerializeGroupPluginDataHook()
