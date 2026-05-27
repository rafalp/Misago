from typing import Protocol

from django.http import HttpRequest

from ...categories.models import Category
from ...plugins.hooks import FilterHook


class GetPrivateThreadsBreadcrumbsHookAction(Protocol):
    """
    Misago function for retrieving a private threads's breadcrumbs.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    The `Category` to retrieve breadcrumbs for.

    # Return value

    A list of `dict`s representing the category's breadcrumbs.
    """

    def __call__(
        self,
        request: HttpRequest,
        category: Category,
    ) -> list[dict]: ...


class GetPrivateThreadsBreadcrumbsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetPrivateThreadsBreadcrumbsHookAction`

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
        action: GetPrivateThreadsBreadcrumbsHookAction,
        request: HttpRequest,
        category: Category,
    ) -> list[dict]: ...


class GetPrivateThreadsBreadcrumbsHook(
    FilterHook[
        GetPrivateThreadsBreadcrumbsHookAction,
        GetPrivateThreadsBreadcrumbsHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    retrieve the private threads list breadcrumbs.

    # Example

    Include extra data in the private threads list breadcrumbs:

    ```python
    from django.http import HttpRequest
    from misago.privatethreads.hooks import get_private_threads_breadcrumbs_hook
    from misago.categories.models import Category


    @get_private_threads_breadcrumbs_hook.append_filter
    def set_private_threads_breadcrumb_icon(
        action, request: HttpRequest, category: Category
    ) -> list[dict]:
        breadcrumbs = action(request, category)
        breadcrumbs[0]["icon"] = "tabler/lock.svg"
        return breadcrumbs
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetPrivateThreadsBreadcrumbsHookAction,
        request: HttpRequest,
        category: Category,
    ) -> list[dict]:
        return super().__call__(action, request, category)


get_private_threads_breadcrumbs_hook = GetPrivateThreadsBreadcrumbsHook()
