from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook


class ReplaceRichTextTokensHookAction(Protocol):
    """
    A standard Misago function used to replace rich-text tokens in pre-rendered
    HTML or the next filter from another plugin.

    # Arguments

    ## `html: str`

    An HTML string in which tokens will be replaced.

    ## `data: dict`

    Data that can be embedded in HTML.

    # Return value

    A `str` with HTML that has its tokens replaced.
    """

    def __call__(self, html: str, data: dict) -> str: ...


class ReplaceRichTextTokensHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: ReplaceRichTextTokensHookAction`

    A standard Misago function used to replace rich-text tokens in pre-rendered
    HTML or the next filter from another plugin.

    See the [action](#action) section for details.

    ## `html: str`

    An HTML string in which tokens will be replaced.

    ## `data: dict`

    Data that can be embedded in HTML.

    # Return value

    A `str` with HTML that has its tokens replaced.
    """

    def __call__(
        self,
        action: ReplaceRichTextTokensHookAction,
        html: str,
        data: dict,
    ) -> str: ...


class ReplaceRichTextTokensHook(
    FilterHook[ReplaceRichTextTokensHookAction, ReplaceRichTextTokensHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to replace rich-text
    tokens in pre-rendered HTML or the next filter from another plugin.

    Tokens are pseudo-HTML elements like `<attachment="..">` that are replaced
    with real HTML markup instead.

    # Example

    The code below implements a custom filter function that replaces default spoiler
    block summary with a custom message:

    ```python
    from misago.parser.context import ParserContext
    from misago.parser.hooks import replace_rich_text_tokens_hook
    from misago.parser.html import SPOILER_SUMMARY


    @replace_rich_text_tokens_hook.append_filter
    def replace_rich_text_spoiler_hoom(
        action,
        html: str,
        data: dict,
    ) -> str:
        if SPOILER_SUMMARY in html:
            html = html.replace(
                SPOILER_SUMMARY, "SPOILER! Click at your own discretion!"
            )

        # Call the next function in chain
        return action(context, html, **kwargs)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: ReplaceRichTextTokensHookAction,
        html: str,
        data: dict,
    ) -> str:
        return super().__call__(action, html, data)


replace_rich_text_tokens_hook = ReplaceRichTextTokensHook()
