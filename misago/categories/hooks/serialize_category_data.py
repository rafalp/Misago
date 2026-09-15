from typing import Any, Protocol

from ...plugins.hooks import FilterHook


class SerializeCategoryDataHookAction(Protocol):
    """
    Misago function used to create a JSON-serializable `dict` with category data
    to cache and use to create a `CategoryProxy` instance.

    # Arguments

    ## `result: dict[str, Any]`

    A `dict` with the category data returned by the queryset.

    # Return value

    A Python `dict` with JSON-serializable category data.
    """

    def __call__(self, result: dict[str, Any]) -> dict[str, Any]: ...


class SerializeCategoryDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    ## `result: dict[str, Any]`

    A `dict` with the category data returned by the queryset.

    # Return value

    A Python `dict` with JSON-serializable category data.
    """

    def __call__(
        self, action: SerializeCategoryDataHookAction, result: dict[str, Any]
    ) -> dict[str, Any]: ...


class SerializeCategoryDataHook(
    FilterHook[SerializeCategoryDataHookAction, SerializeCategoryDataHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to create a
    JSON-serializable `dict` with the category data to populate the `CategoriesProxy`
    and cache across requests.

    # Example

    The code below implements a custom filter function that includes a custom
    data in `plugin_data`:

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
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self, action: SerializeCategoryDataHookAction, result: dict[str, Any]
    ) -> dict[str, Any]:
        return super().__call__(action, result)


serialize_category_data_hook = SerializeCategoryDataHook()
