from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..context import ParserContext


class RenderAstNodeToHtmlHookAction(Protocol):
    """
    A standard Misago function used to create an HTML representation of the abstract
    syntax tree's node or the next filter function from another plugin.

    # Arguments

    ## `context: ParserContext`

    A `ParserContext` data class instance.

    ## `ast_node: dict`

    A `dict` with the AST node to create an HTML representation for.

    ## `metadata: dict`

    A `dict` with metadata.

    # Return value

    A `str` with an HTML representation of the AST node.
    """

    def __call__(
        self,
        context: "ParserContext",
        ast_node: dict,
        metadata: dict,
    ) -> str:
        ...


class RenderAstNodeToHtmlHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: RenderAstNodeToHtmlHookAction`

    A standard Misago function used to create an HTML representation of the abstract
    syntax tree's node or the next filter function from another plugin.

    See the [action](#action) section for details.

    ## `context: ParserContext`

    A `ParserContext` data class instance.

    ## `ast_node: dict`

    A `dict` with the AST node to create an HTML representation for.

    ## `metadata: dict`

    A `dict` with metadata.

    # Return value

    A `str` with an HTML representation of the AST node.
    """

    def __call__(
        self,
        action: RenderAstNodeToHtmlHookAction,
        context: "ParserContext",
        ast_node: dict,
        metadata: dict,
    ) -> str:
        ...


class RenderAstNodeToHtmlHook(
    FilterHook[RenderAstNodeToHtmlHookAction, RenderAstNodeToHtmlHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to create an HTML
    representation of the abstract syntax tree's node.

    # Example

    The code below implements a custom filter function that replaces Twitter media
    links with images:

    ```python
    from misago.parser.context import ParserContext


    @render_ast_node_to_html_hook.append_filter
    def render_twitter_media_link_as_image(
        action: RenderAstNodeToHtmlHookAction,
        context: ParserContext,
        ast_node: dict,
        metadata: dict,
    ) -> str:
        if (
            ast_node["type"] in ("auto-link", "auto-url") and
            is_twitter_media(ast_node["href"])
        ):
            new_ast_node = {
                "type": "auto-link",
                "image": True,
                "href": ast_node["href"],
            }
            return action(context, new_ast_node, metadata)

        # Call the next function in chain
        return action(context, ast_node, metadata)

    def is_twitter_media(href: str) -> bool:
        return bool(
            href.startswith("https://pbs.twimg.com/media/") and
            "?format=jpg&" in href
        )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: RenderAstNodeToHtmlHookAction,
        context: "ParserContext",
        ast_node: dict,
        metadata: dict,
    ) -> str:
        return super().__call__(action, context, ast_node, metadata)


render_ast_node_to_html_hook = RenderAstNodeToHtmlHook()
