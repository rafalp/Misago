from typing import TYPE_CHECKING, Callable, Protocol

from markdown_it.token import Token

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..markup import StateMarkup


class RenderTokensToMarkupHookAction(Protocol):
    """
    A standard Misago function used to convert a token stream into markup.

    # Arguments

    ## `tokens: list[Token]`

    A list of `Token` instances to render as markup.

    ## `rules: list[Callable[[StateMarkup], bool]]`

    A list of `callable`s with rendering rules.

    # Return value

    A `str` with rendered markup.
    """

    def __call__(
        self,
        tokens: list[Token],
        rules: list[Callable[["StateMarkup"], bool]],
    ) -> str: ...


class RenderTokensToMarkupHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: RenderTokensToMarkupHookAction`

    A standard Misago function used to convert a token stream into markup.

    See the [action](#action) section for details.

    ## `tokens: list[Token]`

    A list of `Token` instances to render as text.

    ## `rules: list[Callable[[StateMarkup], bool]]`

    A list of `callable`s with rendering rules.

    # Return value

    A `str` with rendered text.
    """

    def __call__(
        self,
        action: RenderTokensToMarkupHookAction,
        tokens: list[Token],
        rules: list[Callable[["StateMarkup"], bool]],
    ) -> str: ...


class RenderTokensToMarkupHook(
    FilterHook[RenderTokensToMarkupHookAction, RenderTokensToMarkupHookFilter]
):
    """
    This hook wraps the standard function Misago uses to convert a token stream
    into markup.

    Token stream is a list of the `Token` instances from `markdown_it.tokens` module.

    # Example

    The code below implements a custom filter function that includes custom
    rule for token stream rendering:

    ```python
    from typing import Callable

    from markdown_it.tokens import Token
    from misago.parser.hooks import render_tokens_to_markup_hook
    from misago.parser.markup import StateMarkup


    def custom_renderer_rule(state: StateMarkup) -> bool:
        token = state.tokens[state.pos]
        if token.type != "plugin":
            return False

        state.push(tokens[idx].content)
        state.pos += 1

        return True


    @render_tokens_to_markup_hook.append_filter
    def tokenize_with_custom_tokens_processor(
        action,
        tokens: list[Token],
        rules: list[Callable[["StateMarkup"], bool]],
    ) -> str:
        rules.append(("custom_rule", custom_renderer_rule))
        return action(parser, markup, processors)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: RenderTokensToMarkupHookAction,
        tokens: list[Token],
        rules: list[Callable[["StateMarkup"], bool]],
    ) -> str:
        return super().__call__(action, tokens, rules)


render_tokens_to_markup_hook = RenderTokensToMarkupHook()
