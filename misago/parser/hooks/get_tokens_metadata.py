from typing import Protocol

from markdown_it.token import Token

from ...plugins.hooks import FilterHook


class GetTokensMetadataHookAction(Protocol):
    """
    Misago function used to extract metadata from a token stream.

    # Arguments

    ## `tokens: list[Token]`

    A list of tokens ("token stream") from which to extract metadata.

    # Return value

    A `dict` with metadata extracted from the token stream.
    """

    def __call__(self, tokens: list[Token]) -> dict: ...


class GetTokensMetadataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetTokensMetadataHookAction`

    Misago function used to extract metadata from a token stream.

    See the [action](#action) section for details.

    ## `tokens: list[Token]`

    A list of tokens ("token stream") from which to extract metadata.

    # Return value

    A `dict` with metadata extracted from the token stream.
    """

    def __call__(
        self, action: GetTokensMetadataHookAction, tokens: list[Token]
    ) -> dict: ...


class GetTokensMetadataHook(
    FilterHook[GetTokensMetadataHookAction, GetTokensMetadataHookFilter]
):
    """
    This hook wraps the standard function Misago uses to extract metadata
    from a token stream.

    Token stream is a list of the `Token` instances from `markdown_it.tokens` module.

    # Example

    The code below implements a custom filter function that sets `plugin`
    metadata if its found in tokens:

    ```python
    from markdown_it.tokens import Token
    from misago.parser.hooks import get_tokens_metadata_hook

    @get_tokens_metadata_hook.append_filter
    def get_tokens_metadata_plugin(action, tokens: list[Token]) -> dict:
        metadata = action(tokens)

        if plugin_metadata := get_plugin_metadata(tokens):
            metadata["plugin"] = plugin_metadata

        return metadata
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self, action: GetTokensMetadataHookAction, tokens: list[Token]
    ) -> dict:
        return super().__call__(action, tokens)


get_tokens_metadata_hook = GetTokensMetadataHook()
