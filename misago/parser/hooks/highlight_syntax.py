from typing import Protocol

from ...plugins.hooks import FilterHook


class HighlightSyntaxHookAction(Protocol):
    """
    Misago function used to return HTML with highlighted code.

    # Arguments

    ## `syntax: str`

    A syntax to use for code highlighting.

    ## `code: str`

    A code snippet to highlight.

    # Return value

    An HTML string with highlighted code.
    """

    def __call__(self, syntax: str, code: str) -> str: ...


class HighlightSyntaxHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: HighlightSyntaxHookAction`

    Misago function used to return HTML with highlighted code.

    See the [action](#action) section for details.

    ## `syntax: str`

    A syntax to use for code highlighting.

    ## `code: str`

    A code snippet to highlight.

    # Return value

    An HTML string with highlighted code.
    """

    def __call__(
        self,
        action: HighlightSyntaxHookAction,
        syntax: str,
        code: str,
    ) -> str: ...


class HighlightSyntaxHook(
    FilterHook[HighlightSyntaxHookAction, HighlightSyntaxHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to return HTML with
    highlighted code.

    # Example

    The code below implements a custom filter function that replaces the default
    syntax highlighting logic with a custom implementation.

    ```python
    from misago.parser.hooks import highlight_syntax_hook
    from plugin import custom_highlighter


    @highlight_syntax_hook.append_filter
    def replace_rich_text_spoiler_hoom(
        action,
        syntax: str,
        code: str,
    ) -> str:
        return custom_highlighter(syntax, code)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: HighlightSyntaxHookAction,
        syntax: str,
        code: str,
    ) -> str:
        return super().__call__(action, syntax, code)


highlight_syntax_hook = HighlightSyntaxHook()
