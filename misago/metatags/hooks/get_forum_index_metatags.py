from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..metatag import MetaTag


class GetForumIndexMetatagsHookAction(Protocol):
    """
    A standard Misago function used to get metatags for the forum index page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    # Return value

    A Python `dict` with metatags to include in the response HTML.
    """

    def __call__(self, request: HttpRequest) -> dict[str, MetaTag]: ...


class GetForumIndexMetatagsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetForumIndexMetatagsHookAction`

    A standard Misago function used to get metatags for the forum index page.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    # Return value

    A Python `dict` with metatags to include in the response HTML.
    """

    def __call__(
        self,
        action: GetForumIndexMetatagsHookAction,
        request: HttpRequest,
    ) -> dict[str, MetaTag]: ...


class GetForumIndexMetatagsHook(
    FilterHook[GetForumIndexMetatagsHookAction, GetForumIndexMetatagsHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to get metatags for
    the forum index page.

    # Example

    The code below implements a custom filter function that adds a custom
    metatag to the forum index page:

    ```python
    from django.http import HttpRequest
    from misago.metatags.hooks import get_forum_index_metatags_hook
    from misago.metatags.metatag import MetaTag


    @get_forum_index_metatags_hook.append_filter
    def include_custom_metatag(action, request: HttpRequest) -> dict[str, MetaTag]:
        metatags = action(request)
        metatags["custom"] = MetaTag(
            name="og:custom",
            property="twitter:custom",
            itemprop="custom",
            content="custom content",
        )
        return metatags
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetForumIndexMetatagsHookAction,
        request: HttpRequest,
    ) -> dict[str, MetaTag]:
        return super().__call__(action, request)


get_forum_index_metatags_hook = GetForumIndexMetatagsHook()
