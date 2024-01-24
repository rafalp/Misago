from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..context import ParserContext


class CreateAstMetadataHookAction(Protocol):
    """
    A standard Misago function used to extract metadata from the Abstract Syntax Tree
    representation of parsed markup or the next filter function from another plugin.

    # Arguments

    ## `metadata: dict`

    A `dict` with metadata with some keys already pre-set by Misago and
    previous plugins.

    ## `ast: list[dict]`

    A list of `dict`s representing parsed markup.

    ## `context: ParserContext`

    An instance of the `ParserContext` dataclass that contains dependencies
    used at different stages of parsing process.

    # Return value

    A `dict` with completed metadata.
    """

    def __call__(
        self,
        *,
        metadata: dict,
        ast: list[dict],
        context: "ParserContext",
    ) -> dict:
        ...


class CreateAstMetadataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CreateAstMetadataHookAction`

    A standard Misago function used to extract metadata from the Abstract Syntax Tree
    representation of parsed markup or the next filter function from another plugin.

    See the [action](#action) section for details.

    ## `metadata: dict`

    A `dict` with metadata with some keys already pre-set by Misago and
    previous plugins.

    ## `ast: list[dict]`

    A list of `dict`s representing parsed markup.

    ## `context: ParserContext`

    An instance of the `ParserContext` dataclass that contains dependencies
    used at different stages of parsing process.

    # Return value

    A `dict` with completed metadata.
    """

    def __call__(
        self,
        action: CreateAstMetadataHookAction,
        metadata: dict,
        ast: list[dict],
        context: "ParserContext",
    ) -> dict:
        ...


class CreateAstMetadataHook(
    FilterHook[CreateAstMetadataHookAction, CreateAstMetadataHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to extract metadata from
    the Abstract Syntax Tree representation of parsed markup.

    It can be employed to initialize new keys in the `metadata` dictionary before
    the next action call and to retrieve missing data from the database or another
    source after the action.

    # Example

    The code below implements a custom filter function that sets `threads` entry in the
    metadata and populates it with threads:

    ```python
    from misago.parser.context import ParserContext
    from misago.threads.models import Thread


    @create_ast_metadata_hook.append_filter
    def set_ast_metadata_threads(
        action: CreateAstMetadataHookAction,
        metadata: dict,
        ast: list[dict],
        context: ParserContext,
    ) -> dict:
        metadata["threads"] = {
            "ids": set(),
            "threads": {},
        },

        # Call the next function in chain
        metadata = action(metadata, ast, request)

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
        action: CreateAstMetadataHookAction,
        metadata: dict,
        ast: list[dict],
        context: "ParserContext",
    ) -> dict:
        return super().__call__(action, metadata, ast, context)


create_ast_metadata_hook = CreateAstMetadataHook()
