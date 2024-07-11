from typing import Any, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook


class GetCategoriesComponentHookAction(Protocol):
    """
    A standard Misago function used to build a `dict` with data for
    the categories list component, used to display the list of categories on
    the categories page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    # Return value

    A Python `dict` with data for the categories list component.

    Must have at least two keys: `categories` and `template_name`:

    ```python
    {
        "categories": ...,
        "template_name": "misago/categories/list.html"
    }
    ```

    Component will then be rendered with
    """

    def __call__(self, request: HttpRequest) -> dict: ...


class GetCategoriesComponentHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetCategoriesComponentHookAction`

    A standard Misago function used to build a `dict` with data for
    the categories list component, used to display the list of categories on
    the categories page.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    # Return value

    A Python `dict` with data for the categories list component.
    """

    def __call__(
        self, action: GetCategoriesComponentHookAction, request: HttpRequest
    ) -> dict: ...


class GetCategoriesComponentHook(
    FilterHook[GetCategoriesComponentHookAction, GetCategoriesComponentHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to build a `dict`
    with data for the categories list component, used to display the list of
    categories on the categories page.

    # Example

    The code below implements a custom filter function that replaces default
    categories component with a custom one.

    ```python
    from django.http import HttpRequest
    from misago.categories.hooks import get_categories_component_hook


    @get_categories_component_hook.append_filter
    def custom_categories_list(action, request: HttpRequest) -> dict:
        return {
            "categories": [],
            "template_name": "plugin/categories_list.html",
        }
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self, action: GetCategoriesComponentHookAction, request: HttpRequest
    ) -> dict:
        return super().__call__(action, request)


get_categories_component_hook = GetCategoriesComponentHook()
