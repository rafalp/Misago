from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..context import ParserContext


class CompleteMarkupHtmlHookAction(Protocol):
    """
    A standard Misago function used to complete an HTML representation of parsed markup
    or the next filter function from another plugin.

    # Arguments

    ## `html: str`

    An HTML representation of parsed markup to complete.

    # Return value

    A `str` with completed HTML representation of parsed markup.
    """

    def __call__(self, html: str) -> str:
        ...


class CompleteMarkupHtmlHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CompleteMarkupHtmlHookAction`

    A standard Misago function used to complete an HTML representation of parsed markup
    or the next filter function from another plugin.

    See the [action](#action) section for details.

    ## `html: str`

    An HTML representation of parsed markup to complete.

    # Return value

    A `str` with completed HTML representation of parsed markup.
    """

    def __call__(
        self,
        action: CompleteMarkupHtmlHookAction,
        html: str,
    ) -> str:
        ...


class CompleteMarkupHtmlHook(
    FilterHook[CompleteMarkupHtmlHookAction, CompleteMarkupHtmlHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to complete an HTML
    representation of parsed markup.

    Completion process includes:

    - Replacing of placeholder spoiler blocks summaries with messages in active language.
    - Replacing quotation blocks headers with final HTML.

    # Example

    The code below implements a custom filter function that replaces default spoiler
    block summary with a custom message:

    ```python
    from misago.parser.context import ParserContext
    from misago.parser.html import SPOILER_SUMMARY


    @complete_markup_html_hook.append_filter
    def complete_markup_html_with_custom_spoiler-summary(
        action: CompleteMarkupHtmlHookAction,
        html: str,
    ) -> str:
        if SPOILER_SUMMARY in html:
            html = html.replace(
                SPOILER_SUMMARY, "SPOILER! Click at your own discretion!"
            )

        # Call the next function in chain
        return action(context, html)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CompleteMarkupHtmlHookAction,
        html: str,
    ) -> str:
        return super().__call__(action, html)


complete_markup_html_hook = CompleteMarkupHtmlHook()
