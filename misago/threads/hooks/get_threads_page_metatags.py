from typing import Protocol

from django.http import HttpRequest

from ...metatags.metatag import MetaTag
from ...plugins.hooks import FilterHook


class GetThreadsPageMetatagsHookAction(Protocol):
    """
    A standard Misago function used to get metatags for the threads page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `context: dict`

    The context to render the page with.

    # Return value

    A Python `dict` with metatags to include in the response HTML.
    """

    def __call__(self, request: HttpRequest, context: dict) -> dict[str, MetaTag]: ...


class GetThreadsPageMetatagsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadsPageMetatagsHookAction`

    A standard Misago function used to get metatags for the threads page.

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
        action: GetThreadsPageMetatagsHookAction,
        request: HttpRequest,
        context: dict,
    ) -> dict[str, MetaTag]: ...


class GetThreadsPageMetatagsHook(
    FilterHook[GetThreadsPageMetatagsHookAction, GetThreadsPageMetatagsHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to get
    metatags for the threads page.

    # Example

    The code below implements a custom filter function that sets a custom
    metatag on the threads page, if its not used as the forum index page:

    ```python
    from django.http import HttpRequest
    from misago.threads.hooks import get_threads_page_metatags_hook
    from misago.metatags.metatag import MetaTag


    @get_threads_page_metatags_hook.append_filter
    def include_custom_metatag(action, request: HttpRequest, context) -> dict[str, MetaTag]:
        metatags = action(request)

        if not context["is_index"]:
            metatags["description"] = MetaTag(
                name="og:description",
                property="twitter:description",
                content="Lorem ipsum dolor met.",
            )

        return metatags
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadsPageMetatagsHookAction,
        request: HttpRequest,
        context: dict,
    ) -> dict[str, MetaTag]:
        return super().__call__(action, request, context)


get_threads_page_metatags_hook = GetThreadsPageMetatagsHook()
