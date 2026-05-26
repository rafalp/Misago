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

    A list of `dict`s representing the category's breadcrumbs.
    """

    def __call__(
        self,
        request: HttpRequest,
        category: Category,
        include_category: bool = False,
    ) -> list[dict]: ...


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

    # Return value

    A list of `dict`s representing the category's breadcrumbs.
    """

    def __call__(
        self,
        action: GetCategoryBreadcrumbsHookAction,
        request: HttpRequest,
        category: Category,
        include_category: bool = False,
    ) -> list[dict]: ...


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

    Include extra data in a category's breadcrumbs:

    ```python
    from django.http import HttpRequest
    from misago.categorys.hooks import get_category_breadcrumbs_hook
    from misago.categorys.models import Category


    @get_category_breadcrumbs_hook.append_filter
    def set_category_breadcrumb_icon(
        action,
        request: HttpRequest,
        category: Category,
        include_category: bool = False,
    ) -> list[dict]:
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
    ) -> list[dict]:
        return super().__call__(action, request, category, include_category)


get_category_breadcrumbs_hook = GetCategoryBreadcrumbsHook()
