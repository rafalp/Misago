from typing import Protocol

from ...plugins.hooks import FilterHook


class GetCategoriesQueryValuesHookAction(Protocol):
    """
    A standard Misago function used to retrieve a set of arguments for the `values`
    call on the categories queryset.

    # Return value

    A Python `set` with names of the `Category` model fields to include in the queryset.
    """

    def __call__(self) -> set[str]: ...


class GetCategoriesQueryValuesHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Return value

    A Python `set` with names of the `Category` model fields to include in the queryset.
    """

    def __call__(self, action: GetCategoriesQueryValuesHookAction) -> set[str]: ...


class GetCategoriesQueryValuesHook(
    FilterHook[GetCategoriesQueryValuesHookAction, GetCategoriesQueryValuesHookFilter]
):
    """
    This hook wraps the standard Misago function used to retrieve a set of arguments for
    the `values` call on the categories queryset.

    # Example

    The code below implements a custom filter function that includes the `plugin_data`
    field in the queryset.

    ```python
    from misago.categories.hooks import get_categories_query_values_hook


    @get_categories_query_values_hook.append_filter
    def include_plugin_data_in_query(action) -> set[str]:
        fields = action(groups)
        fields.add("plugin_data")
        return fields
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(self, action: GetCategoriesQueryValuesHookAction) -> dict:
        return super().__call__(action)


get_categories_query_values_hook = GetCategoriesQueryValuesHook()
