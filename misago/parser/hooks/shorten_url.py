from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook


class ShortenURLHookAction(Protocol):
    """
    Misago function used to shorten URLs in text or the next filter
    function from another plugin.

    # Arguments

    ## `url: str`

    A `str` with URL to be shortened.

    # Return value

    A `str` with the shortened URL.
    """

    def __call__(self, url: str) -> str: ...


class ShortenURLHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: ShortenURLHookAction`

    Misago function used to shorten URLs in text or the next filter
    function from another plugin.

    See the [action](#action) section for details.

    ## `url: str`

    A `str` with URL to be shortened.

    # Return value

    A `str` with the shortened URL.
    """

    def __call__(self, action: ShortenURLHookAction, url: str) -> str: ...


class ShortenURLHook(FilterHook[ShortenURLHookAction, ShortenURLHookFilter]):
    """
    This hook wraps the standard function that Misago uses to shorten URLs in text.

    # Example

    The code below implements a custom filter function that disables shortening
    for the Wikipedia URLS:

    ```python
    from misago.parser.hooks import shorten_url_hook


    @shorten_url_hook.append_filter
    def shorten_url(action, url: str) -> str:
        if "wikipedia" in url:
            return url

        return action(url)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(self, action: ShortenURLHookAction, url: str) -> str:
        return super().__call__(action, url)


shorten_url_hook = ShortenURLHook()
