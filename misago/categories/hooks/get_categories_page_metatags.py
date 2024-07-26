from typing import Protocol

from django.http import HttpRequest

from ...metatags.metatag import MetaTag
from ...plugins.hooks import FilterHook


class GetCategoriesPageMetatagsHookAction(Protocol):
    """
    A standard Misago function used to get metatags for the categories page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `context: dict`

    The context to render the page with.

    # Return value

    A Python `dict` with metatags to include in the response HTML.
    """

    def __call__(self, request: HttpRequest, context: dict) -> dict[str, MetaTag]: ...


class GetCategoriesPageMetatagsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetCategoriesPageMetatagsHookAction`

    A standard Misago function used to get metatags for the categories page.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `context: dict`

    The context to render the page with.

    # Return value

    A Python `dict` with metatags to include in the response HTML.
    """

    def __call__(
        self,
        action: GetCategoriesPageMetatagsHookAction,
        request: HttpRequest,
        context: dict,
    ) -> dict[str, MetaTag]: ...


class GetCategoriesPageMetatagsHook(
    FilterHook[GetCategoriesPageMetatagsHookAction, GetCategoriesPageMetatagsHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to get
    metatags for the categories page.

    # Example

    The code below implements a custom filter function that sets a custom
    metatag on the categories page, if its not used as the forum index page:

    ```python
    from django.http import HttpRequest
    from misago.categories.hooks import get_categories_page_metatags_hook
    from misago.metatags.metatag import MetaTag


    @get_categories_page_metatags_hook.append_filter
    def include_custom_metatag(action, request: HttpRequest, context) -> dict[str, MetaTag]:
        metatags = action(request)

        if not context["is_index"]:
            categories = len(context["categories_list"])
            metatags["description"] = MetaTag(
                name="og:description",
                property="twitter:description",
                content=f"There are currently {categories} categories on our forums.",
            )

        return metatags
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetCategoriesPageMetatagsHookAction,
        request: HttpRequest,
        context: dict,
    ) -> dict[str, MetaTag]:
        return super().__call__(action, request, context)


get_categories_page_metatags_hook = GetCategoriesPageMetatagsHook()
