from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..metatag import MetaTag


class GetDefaultMetatagsHookAction(Protocol):
    """
    A standard Misago function used to get default metatags for all pages.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    # Return value

    A Python `dict` with metatags to include in the response HTML.
    """

    def __call__(self, request: HttpRequest) -> dict[str, MetaTag]: ...


class GetDefaultMetatagsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetDefaultMetatagsHookAction`

    A standard Misago function used to get default metatags for all pages.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    # Return value

    A Python `dict` with metatags to include in the response HTML.
    """

    def __call__(
        self,
        action: GetDefaultMetatagsHookAction,
        request: HttpRequest,
    ) -> dict[str, MetaTag]: ...


class GetDefaultMetatagsHook(
    FilterHook[GetDefaultMetatagsHookAction, GetDefaultMetatagsHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to get default
    metatags for all pages.

    # Example

    The code below implements a custom filter function that adds a custom
    metatag to all pages:

    ```python
    from django.http import HttpRequest
    from misago.metatags.hooks import get_default_metatags_hook
    from misago.metatags.metatag import MetaTag


    @get_default_metatags_hook.append_filter
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
        action: GetDefaultMetatagsHookAction,
        request: HttpRequest,
    ) -> dict[str, MetaTag]:
        return super().__call__(action, request)


get_default_metatags_hook = GetDefaultMetatagsHook()
