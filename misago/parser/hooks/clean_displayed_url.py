from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook


class CleanDisplayedURLHookAction(Protocol):
    """
    A standard Misago function used to clean URLs for display in HTML
    or the next filter function from another plugin.

    # Arguments

    ## `url: str`

    A `str` with URL to be cleaned.

    # Return value

    A `str` with the cleaned URL.
    """

    def __call__(self, url: str) -> str: ...


class CleanDisplayedURLHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CleanDisplayedURLHookAction`

    A standard Misago function used to clean URLs for display in HTML
    or the next filter function from another plugin.

    See the [action](#action) section for details.

    ## `url: str`

    A `str` with URL to be cleaned.

    # Return value

    A `str` with the cleaned URL.
    """

    def __call__(self, action: CleanDisplayedURLHookAction, url: str) -> str: ...


class CleanDisplayedURLHook(
    FilterHook[CleanDisplayedURLHookAction, CleanDisplayedURLHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to clean URLs for
    display in HTML

    # Example

    The code below implements a custom filter function that disables cleaning
    for the Wikipedia URLS:

    ```python
    from misago.parser.hooks import clean_displayed_url_hook


    @clean_displayed_url_hook.append_filter
    def clean_displayed_url(action, url: str) -> str:
        if "wikipedia" in url:
            return url

        return action(url)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(self, action: CleanDisplayedURLHookAction, url: str) -> str:
        return super().__call__(action, url)


clean_displayed_url_hook = CleanDisplayedURLHook()
