from typing import Protocol

from django.http import HttpRequest

from ...categories.models import Category
from ...plugins.hooks import FilterHook


class GetCategoryThreadsPageSubcategoriesHookAction(Protocol):
    """
    A standard Misago function used to build a `dict` with data for
    the categories list component, used to display the list of subcategories on
    the category threads page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    A category instance.

    # Return value

    A Python `dict` with data for the categories list component.

    Must have at least two keys: `categories` and `template_name`:

    ```python
    {
        "categories": ...,
        "template_name": "misago/category/subcategories.html"
    }
    ```

    To suppress categories lists on a page, return `None`.
    """

    def __call__(self, request: HttpRequest, category: Category) -> dict | None: ...


class GetCategoryThreadsPageSubcategoriesHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetCategoryThreadsPageSubcategoriesHookAction`

    A standard Misago function used to build a `dict` with data for
    the categories list component, used to display the list of subcategories on
    the category threads page.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    A category instance.

    # Return value

    A Python `dict` with data for the categories list component.

    Must have at least two keys: `categories` and `template_name`:

    ```python
    {
        "categories": ...,
        "template_name": "misago/category/subcategories.html"
    }
    ```

    To suppress categories lists on a page, return `None`.
    """

    def __call__(
        self,
        action: GetCategoryThreadsPageSubcategoriesHookAction,
        request: HttpRequest,
        category: Category,
    ) -> dict | None: ...


class GetCategoryThreadsPageSubcategoriesHook(
    FilterHook[
        GetCategoryThreadsPageSubcategoriesHookAction,
        GetCategoryThreadsPageSubcategoriesHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to build a `dict`
    with data for the categories list component, used to display the list of
    subcategories on the category threads page.

    # Example

    The code below implements a custom filter function that replaces full
    subcategories component's template with a custom one

    ```python
    from django.http import HttpRequest
    from misago.categories.models import Category
    from misago.threads.hooks import get_category_threads_page_subcategories_hook


    @get_category_threads_page_subcategories_hook.append_filter
    def customize_subcategories_template(
        action, request: HttpRequest, category: Category
    ) -> dict | None:
        data = action(request, category)
        data["template_name"] = "plugin/subcategories.html"
        return data
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetCategoryThreadsPageSubcategoriesHookAction,
        request: HttpRequest,
        category: Category,
    ) -> dict | None:
        return super().__call__(action, request, category)


get_category_threads_page_subcategories_hook = GetCategoryThreadsPageSubcategoriesHook(
    cache=False
)
