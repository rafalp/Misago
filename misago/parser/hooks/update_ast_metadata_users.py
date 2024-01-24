from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..context import ParserContext


class UpdateAstMetadataUsersHookAction(Protocol):
    """
    A standard Misago function used to update metadata with users from the database,
    or the next filter function from another plugin.

    # Arguments

    ## `metadata: dict`

    A `dict` with metadata to update.

    ## `context: ParserContext`

    An instance of the `ParserContext` data class that contains dependencies
    used during parsing.
    """

    def __call__(
        self,
        *,
        metadata: dict,
        context: "ParserContext",
    ) -> None:
        ...


class UpdateAstMetadataUsersHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: UpdateAstMetadataUsersHookAction`

    A standard Misago function used to update metadata with users from the database,
    or the next filter function from another plugin.

    See the [action](#action) section for details.

    ## `metadata: dict`

    A `dict` with metadata to update.

    ## `context: ParserContext`

    An instance of the `ParserContext` data class that contains dependencies
    used during parsing.
    """

    def __call__(
        self,
        action: UpdateAstMetadataUsersHookAction,
        metadata: dict,
        context: "ParserContext",
    ) -> None:
        ...


class UpdateAstMetadataUsersHook(
    FilterHook[UpdateAstMetadataUsersHookAction, UpdateAstMetadataUsersHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to update metadata
    with users from the database.

    # Example

    The code below implements a custom filter function that populates `threads` entry in
    the metadata with threads ids extracted them the `url` nodes:

    ```python
    from django.urls import Resolver404, resolve
    from misago.parser.context import ParserContext


    @update_ast_metadata_from_node_hook.append_filter
    def update_ast_metadata_threads(
        action: UpdateAstMetadataUsersHookAction,
        metadata: dict,
        ast_node: dict,
        context: ParserContext,
    ) -> None:
        if ast_node["type"] in ("url", "url-bbcode", "autolink", "auto-url"):
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
        action: UpdateAstMetadataUsersHookAction,
        metadata: dict,
        context: "ParserContext",
    ) -> None:
        return super().__call__(action, metadata, context)


update_ast_metadata_users_hook = UpdateAstMetadataUsersHook()
