from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..context import ParserContext


class RenderAstNodeToPlainTextHookAction(Protocol):
    """
    A standard Misago function used to create a plain text representation of the
    abstract syntax tree's node or the next filter function from another plugin.

    # Arguments

    ## `context: ParserContext`

    A `ParserContext` data class instance.

    ## `ast_node: dict`

    A `dict` with the AST node to create a plain text representation for.

    ## `metadata: dict`

    A `dict` with metadata.

    ## `text_format: str | None = None`

    A `str` with target plain text format, or `None` if not provided.

    # Return value

    A `str` with a plain text representation of the AST node.
    """

    def __call__(
        self,
        context: "ParserContext",
        ast_node: dict,
        metadata: dict,
        text_format: str | None = None,
    ) -> str: ...


class RenderAstNodeToPlainTextHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: RenderAstNodeToPlainTextHookAction`

    A standard Misago function used to create a plain text representation of the
    abstract syntax tree's node or the next filter function from another plugin.

    See the [action](#action) section for details

    ## `context: ParserContext`

    A `ParserContext` data class instance.

    ## `ast_node: dict`

    A `dict` with the AST node to create a plain text representation for.

    ## `metadata: dict`

    A `dict` with metadata.

    ## `text_format: str | None = None`

    A `str` with target plain text format, or `None` if not provided.

    # Return value

    A `str` with a plain text representation of the AST node.
    """

    def __call__(
        self,
        action: RenderAstNodeToPlainTextHookAction,
        context: "ParserContext",
        ast_node: dict,
        metadata: dict,
        text_format: str | None = None,
    ) -> str: ...


class RenderAstNodeToPlainTextHook(
    FilterHook[RenderAstNodeToPlainTextHookAction, RenderAstNodeToPlainTextHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to create a plain text
    representation of the abstract syntax tree's node.

    # Example

    The code below implements a custom filter function that only inserts images
    alt text in the text document:

    ```python
    from misago.parser.context import ParserContext
    from misago.parser.hooks import render_ast_node_to_plaintext_hook


    @render_ast_node_to_plaintext_hook.append_filter
    def render_images_alt_text_only(
        action: RenderAstNodeToPlainTextHookAction,
        context: ParserContext,
        ast_node: dict,
        metadata: dict,
        text_format: str | None = None,
    ) -> str:
        if ast_node["type"] in ("image", "image-bbcode"):
            return ast_node["alt"] or ""

        # Call the next function in chain
        return action(context, ast_node, metadata, text_format)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: RenderAstNodeToPlainTextHookAction,
        context: "ParserContext",
        ast_node: dict,
        metadata: dict,
        text_format: str | None = None,
    ) -> str:
        return super().__call__(action, context, ast_node, metadata, text_format)


render_ast_node_to_plaintext_hook = RenderAstNodeToPlainTextHook()
