from typing import Protocol

from django.contrib.auth import get_user_model
from django.http import HttpRequest

from ...plugins.hooks import FilterHook

User = get_user_model()


class UpdateAstMetadataFromNodeHookAction(Protocol):
    """
    A standard Misago function used to update metadata from an individual node
    from the Abstract Syntax Tree representation of parsed markup.

    # Arguments

    ## `metadata: dict`

    A `dict` with metadata to update.

    ## `ast_node: dict`

    A `dict` with the individual node.

    ## `user: User | None = None`

    A `User` instance with the parsed text's author or `None` if not provided.

    ## `request: HttpRequest | None = None`

    The request object or `None` if it was not provided.
    """

    def __call__(
        self,
        *,
        metadata: dict,
        ast_node: dict,
        request: HttpRequest | None = None,
    ) -> None:
        ...


class UpdateAstMetadataFromNodeHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: UpdateAstMetadataFromNodeHookAction`

    A standard Misago function used to update metadata from an individual node
    from the Abstract Syntax Tree representation of parsed markup or the next
    filter function from another plugin.

    See the [action](#action) section for details.

    ## `metadata: dict`

    A `dict` with metadata to update.

    ## `ast_node: dict`

    A `dict` with the individual node.

    ## `user: User | None = None`

    A `User` instance with the parsed text's author or `None` if not provided.

    ## `request: HttpRequest | None = None`

    The request object or `None` if it was not provided.
    """

    def __call__(
        self,
        action: UpdateAstMetadataFromNodeHookAction,
        metadata: dict,
        ast_node: dict,
        request: HttpRequest | None = None,
    ) -> None:
        ...


class UpdateAstMetadataFromNodeHook(
    FilterHook[UpdateAstMetadataFromNodeHookAction, UpdateAstMetadataFromNodeHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to update metadata from an
    individual node from the Abstract Syntax Tree representation of parsed markup.

    # Example

    The code below implements a custom filter function that populates `threads` entry in
    the metadata with threads ids extracted them the `url` nodes:

    ```python
    from django.contrib.auth import get_user_model
    from django.http import HttpRequest
    from django.urls import Resolver404, resolve

    User = get_user_model()


    @update_ast_metadata_from_node_hook.append_filter
    def update_ast_metadata_threads(
        action: UpdateAstMetadataFromNodeHookAction,
        metadata: dict,
        ast_node: dict,
        user: User | None = None,
        request: HttpRequest | None = None,
    ) -> None:
        if ast_node["type"] in ("url", "url-bbcode", "autolink", "auto-url"):
            if thread_id := get_thread_id_from_url(ast_node["href"])
                metadata["threads"]["ids"].add(thread_id)

        action(ast_node, metadata, request)


    def get_thread_id_from_url(url: str) -> int | None:
        try:
            resolver_match = resolve(url)
        except Resolver404:
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
        metadata: dict,
        ast_node: dict,
        user: User | None = None,
        request: HttpRequest | None = None,
    ) -> None:
        return super().__call__(action, metadata, ast_node, user, request)


update_ast_metadata_from_node_hook = UpdateAstMetadataFromNodeHook()
