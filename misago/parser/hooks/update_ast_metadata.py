from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..context import ParserContext


class UpdateAstMetadataHookAction(Protocol):
    """
    A standard Misago function used to update the metadata with data from the Abstract
    Syntax Tree representation of parsed markup or the next filter function
    from another plugin.

    # Arguments

    ## `context: ParserContext`

    An instance of the `ParserContext` data class that contains dependencies
    used during parsing.

    ## `ast: list[dict]`

    A list of `dict`s representing parsed markup.

    ## `metadata: dict`

    A `dict` with metadata with some keys already pre-set by Misago and
    previous plugins.

    # Return value

    A `dict` with completed metadata.
    """

    def __call__(
        self,
        *,
        context: "ParserContext",
        ast: list[dict],
        metadata: dict,
    ) -> dict: ...


class UpdateAstMetadataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: UpdateAstMetadataHookAction`

    A standard Misago function used to update the metadata with data from the Abstract
    Syntax Tree representation of parsed markup or the next filter function
    from another plugin.

    See the [action](#action) section for details.

    ## `context: ParserContext`

    An instance of the `ParserContext` data class that contains dependencies
    used during parsing.

    ## `ast: list[dict]`

    A list of `dict`s representing parsed markup.

    ## `metadata: dict`

    A `dict` with metadata with some keys already pre-set by Misago and
    previous plugins.

    # Return value

    A `dict` with completed metadata.
    """

    def __call__(
        self,
        action: UpdateAstMetadataHookAction,
        context: "ParserContext",
        ast: list[dict],
        metadata: dict,
    ) -> dict: ...


class UpdateAstMetadataHook(
    FilterHook[UpdateAstMetadataHookAction, UpdateAstMetadataHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to update the metadata
    with data from the Abstract Syntax Tree representation of parsed markup.

    It can be employed to initialize new keys in the `metadata` dictionary before
    the next action call and to retrieve missing data from the database or another
    source after the action.

    # Example

    The code below implements a custom filter function that sets `threads` entry in the
    metadata and populates it with threads:

    ```python
    from misago.parser.context import ParserContext
    from misago.parser.hooks import update_ast_metadata_hook
    from misago.threads.models import Thread


    @update_ast_metadata_hook.append_filter
    def update_ast_metadata_threads(
        action,
        context: ParserContext,
        ast: list[dict],
        metadata: dict,
    ) -> dict:
        metadata["threads"] = {
            "ids": set(),
            "threads": {},
        },

        # Call the next function in chain
        metadata = action(context, ast, metadata)

        threads_ids = metadata["threads"]["ids"]
        if threads_ids and len(threads_ids) < 30:  # Safety limit
            for thread in Thread.objects.filter(id__in=threads_ids):
                metadata["threads"]["threads"][thread.id] = thread

        return metadata
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: UpdateAstMetadataHookAction,
        context: "ParserContext",
        ast: list[dict],
        metadata: dict,
    ) -> dict:
        return super().__call__(action, context, ast, metadata)


update_ast_metadata_hook = UpdateAstMetadataHook()
