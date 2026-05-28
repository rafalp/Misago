from typing import Protocol

from django.http import HttpRequest

from ...categories.models import Category
from ...plugins.hooks import FilterHook


class GetCategoryBreadcrumbsHookAction(Protocol):
    """
    Misago function for retrieving a category's breadcrumbs.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    The `Category` to retrieve breadcrumbs for.

    ## `include_category: bool = False`

    Include `category` as the last breadcrumb.

    Defaults to `False`.

    # Return value

    A `dict` with a breadcrumbs template component.
    """

    def __call__(
        self,
        request: HttpRequest,
        category: Category,
        include_category: bool = False,
    ) -> dict: ...


class GetCategoryBreadcrumbsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetCategoryBreadcrumbsHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    The `Category` to retrieve breadcrumbs for.

    ## `include_category: bool = False`

    Include `category` as the last breadcrumb.

    Defaults to `False`.

    # Return value

    A `dict` with a breadcrumbs template component.
    """

    def __call__(
        self,
        action: GetCategoryBreadcrumbsHookAction,
        request: HttpRequest,
        category: Category,
        include_category: bool = False,
    ) -> dict: ...


class GetCategoryBreadcrumbsHook(
    FilterHook[
        GetCategoryBreadcrumbsHookAction,
        GetCategoryBreadcrumbsHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    retrieve a category's breadcrumbs.

    # Example

    Change the icon used for the category breadcrumb:

    ```python
    from django.http import HttpRequest
    from misago.categories.models import Category
    from misago.threads.hooks import get_category_breadcrumbs_hook


    @get_category_breadcrumbs_hook.append_filter
    def set_category_breadcrumb_icon(
        action,
        request: HttpRequest,
        category: Category,
        include_category: bool = False,
    ) -> dict:
        breadcrumbs = action(request, category, include_category)
        if include_category and category.is_locked:
            breadcrumbs[-1]["icon"] = "tabler/lock.svg"
        return breadcrumbs
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetCategoryBreadcrumbsHookAction,
        request: HttpRequest,
        category: Category,
        include_category: bool = False,
    ) -> dict:
        return super().__call__(action, request, category, include_category)


get_category_breadcrumbs_hook = GetCategoryBreadcrumbsHook()
