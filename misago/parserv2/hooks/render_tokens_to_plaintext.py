from typing import TYPE_CHECKING, Callable, Protocol

from markdown_it import MarkdownIt
from markdown_it.token import Token

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..plaintext import RendererPlaintext


class RenderTokensToPlaintextHookAction(Protocol):
    """
    A standard Misago function used to convert a token stream into plain text.

    # Arguments

    ## `tokens: list[Token]`

    A list of `Token` instances to render as text.

    ## `rules: list[tuple[str, Callable[[RendererPlaintext, list[Token], int], str | None]]]`

    A list of `str`-`callable` pairs where `str` is the name of a `Token` type and `callable` implements the rendering logic.

    # Return value

    A `str` with rendered text.
    """

    def __call__(
        self,
        tokens: list[Token],
        rules: list[
            tuple[str, Callable[["RendererPlaintext", list[Token], int], str | None]]
        ],
    ) -> str: ...


class RenderTokensToPlaintextHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: RenderTokensToPlaintextHookAction`

    A standard Misago function used to convert a token stream into plain text.

    See the [action](#action) section for details.

    ## `tokens: list[Token]`

    A list of `Token` instances to render as text.

    ## `rules: list[tuple[str, Callable[[RendererPlaintext, list[Token], int], str | None]]]`

    A list of `str`-`callable` pairs where `str` is the name of a `Token` type and `callable` implements the rendering logic.

    # Return value

    A `str` with rendered text.
    """

    def __call__(
        self,
        action: RenderTokensToPlaintextHookAction,
        tokens: list[Token],
        rules: list[
            tuple[str, Callable[["RendererPlaintext", list[Token], int], str | None]]
        ],
    ) -> str: ...


class RenderTokensToPlaintextHook(
    FilterHook[RenderTokensToPlaintextHookAction, RenderTokensToPlaintextHookFilter]
):
    """
    This hook wraps the standard function Misago uses to convert a token stream
    into plain text.

    Token stream is a list of the `Token` instances from `markdown_it.tokens` module.

    # Example

    The code below implements a custom filter function that includes custom
    rule for token stream rendering:

    ```python
    from typing import Callable

    from markdown_it.tokens import Token
    from misago.parser.hooks import render_tokens_to_plaintext_hook
    from misago.parser.plaintext import RendererPlaintext


    def custom_renderer_rule(
        renderer: RendererPlaintext, tokens: list[Token], idx: int
    ) -> str | None:
        return "\n" + tokens[idx].content


    @render_tokens_to_plaintext_hook.append_filter
    def tokenize_with_custom_tokens_processor(
        action,
        tokens: list[Token],
        rules: list[tuple[str, Callable[[RendererPlaintext, list[Token], int], str | None]]],
    ) -> str:
        rules.append(("custom_rule", custom_renderer_rule))
        return action(parser, markup, processors)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: RenderTokensToPlaintextHookAction,
        tokens: list[Token],
        rules: list[
            tuple[str, Callable[["RendererPlaintext", list[Token], int], str | None]]
        ],
    ) -> str:
        return super().__call__(action, tokens, rules)


render_tokens_to_plaintext_hook = RenderTokensToPlaintextHook()
