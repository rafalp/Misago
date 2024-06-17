from typing import Any, Protocol

from ...plugins.hooks import FilterHook


class GetCategoryDataHookAction(Protocol):
    """
    A standard Misago function used to build a `dict` with category result from queryset's
    result.

    # Arguments

    ## `result: dict[str, Any]`

    A `dict` with category data returned by the queryset.

    # Return value

    A Python `dict` with category data to cache and use by Misago.
    """

    def __call__(self, result: dict[str, Any]) -> dict[str, Any]: ...


class GetCategoryDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    ## `result: dict[str, Any]`

    A `dict` with category data returned by the queryset.

    # Return value

    A Python `dict` with category data to cache and use by Misago.
    """

    def __call__(
        self, action: GetCategoryDataHookAction, result: dict[str, Any]
    ) -> dict[str, Any]: ...


class GetCategoryDataHook(
    FilterHook[GetCategoryDataHookAction, GetCategoryDataHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to build a `dict` with
    category data from queryset's result.

    # Example

    The code below implements a custom filter function that includes a custom
    dict entry using `plugin_data`:

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
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self, action: GetCategoryDataHookAction, result: dict[str, Any]
    ) -> dict[str, Any]:
        return super().__call__(action, result)


get_category_data_hook = GetCategoryDataHook()
