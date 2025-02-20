from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..context import ParserContext


class UpdateAstMetadataFromNodeHookAction(Protocol):
    """
    A standard Misago function used to update the metadata from an individual node
    from the Abstract Syntax Tree representation of parsed markup or the next
    filter function from another plugin.

    # Arguments

    ## `context: ParserContext`

    An instance of the `ParserContext` data class that contains dependencies
    used during parsing.

    ## `ast_node: dict`

    A `dict` with the individual node.

    ## `metadata: dict`

    A `dict` with metadata to update.
    """

    def __call__(
        self,
        *,
        context: "ParserContext",
        ast_node: dict,
        metadata: dict,
    ) -> None: ...


class UpdateAstMetadataFromNodeHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: UpdateAstMetadataFromNodeHookAction`

    A standard Misago function used to update the metadata from an individual node
    from the Abstract Syntax Tree representation of parsed markup or the next
    filter function from another plugin.

    See the [action](#action) section for details.

    ## `context: ParserContext`

    An instance of the `ParserContext` data class that contains dependencies
    used during parsing.

    ## `ast_node: dict`

    A `dict` with the individual node.

    ## `metadata: dict`

    A `dict` with metadata to update.
    """

    def __call__(
        self,
        action: UpdateAstMetadataFromNodeHookAction,
        context: "ParserContext",
        ast_node: dict,
        metadata: dict,
    ) -> None: ...


class UpdateAstMetadataFromNodeHook(
    FilterHook[UpdateAstMetadataFromNodeHookAction, UpdateAstMetadataFromNodeHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to update the metadata
    from an individual node from the Abstract Syntax Tree representation
    of parsed markup.

    # Example

    The code below implements a custom filter function that populates `threads` entry in
    the metadata with threads ids extracted them the `url` nodes:

    ```python
    from django.urls import Resolver404, resolve
    from misago.parser.hooks import update_ast_metadata_from_node_hook
    from misago.parser.context import ParserContext


    @update_ast_metadata_from_node_hook.append_filter
    def update_ast_metadata_threads(
        action,
        context: ParserContext,
        ast_node: dict,
        metadata: dict,
    ) -> None:
        if ast_node["type"] in ("url", "url-bbcode", "auto-link", "auto-url"):
            if thread_id := get_thread_id_from_url(context, ast_node["href"])
                metadata["threads"]["ids"].add(thread_id)

        action(ast_node, metadata, request)


    def get_thread_id_from_url(context: ParserContext, url: str) -> int | None:
        try:
            resolver_match = resolve(url)
        except Resolver404:
            return None

        if not context.forum_address.is_inbound_link(url):
            return None

        if (
            resolver_match.namespace == "misago" and
            resolver_match.url_name == "thread" and
            resolver_match.captured_kwargs.get("pk")
        )
            return resolver_match.captured_kwargs.get("pk")

        return None
    ```

    For an explanation on `metadata["threads"]`, please see the
    `create_ast_metadata_hook` reference.
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: UpdateAstMetadataFromNodeHookAction,
        context: "ParserContext",
        ast_node: dict,
        metadata: dict,
    ) -> None:
        return super().__call__(action, context, ast_node, metadata)


update_ast_metadata_from_node_hook = UpdateAstMetadataFromNodeHook()
