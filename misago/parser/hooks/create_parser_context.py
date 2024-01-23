from typing import Protocol

from django.http import HttpRequest

from ...permissions.proxy import UserPermissionsProxy
from ...plugins.hooks import FilterHook


class CreateParserContextHookAction(Protocol):
    """
    A standard Misago function used to create a dictionary with Parser Context
    or the next filter function from another plugin.

    # Arguments

    ## `request: HttpRequest | None = None`

    The request object or `None` if it was not provided.

    ## `user_permissions: UserPermissionsProxy | None = None`

    A `UserPermissionsProxy` instance with `user` and `permissions` attributes
    for the parsed text's author or `None` if not provided.

    ## `settings: dict | None`

    A `UserPermissionsProxy` instance with `user` and `permissions` attributes
    for the parsed text's author or `None` if not provided.

    ## `cache_versions: dict | None`

    A `UserPermissionsProxy` instance with `user` and `permissions` attributes
    for the parsed text's author or `None` if not provided.

    # Return value

    A Python `dict` with the Parser Context:

    ```python
    class ParserContext(TypedDict):
        request: HttpRequest | None = None,
        user_permissions: UserPermissionsProxy | None = None,
        settings: dict | None = None,
        cache_versions: dict | None = None,
    ```
    """

    def __call__(
        self,
        *,
        request: HttpRequest | None = None,
        user_permissions: UserPermissionsProxy | None = None,
        settings: dict | None = None,
        cache_versions: dict | None = None,
    ) -> dict:
        ...


class CreateParserContextHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CreateParserContextHookAction`

    A standard Misago function used to create a markup parser instance or the
    next filter function from another plugin.

    See the [action](#action) section for details.

    ## `block_patterns: list[Pattern]`

    A list of `Pattern` instances of block patterns to be used by the parser.

    ## `inline_patterns: list[Pattern]`

    A list of `Pattern` instances of inline patterns to be used by the parser.

    ## `post_processors: list[Callable[[Parser, list[dict]], list[dict]]]`

    A list of post-processor functions called by the parser to finalize the AST.

    A post-processor function should have the following signature:

    ```python
    def custom_postprocessor(parser: Parser, ast: list[dict]) -> list[dict]:
        # Do something with the 'ast'...
        return ast
    ```

    ## `user: User | None = None`

    A `User` instance with the parsed text's author or `None` if not provided.

    ## `request: HttpRequest | None = None`

    The request object or `None` if it was not provided.

    ## `content_type: str | None = None`

    A `str` with the name of the content type to be parsed (e.g., `post` or `signature`)
    or `None` if not provided.

    # Return value

    An instance of the `Parser` class from the `mistune` library.
    """

    def __call__(
        self,
        action: CreateParserContextHookAction,
        *,
        request: HttpRequest | None = None,
        user_permissions: UserPermissionsProxy | None = None,
        settings: dict | None = None,
        cache_versions: dict | None = None,
    ) -> dict:
        ...


class CreateParserContextHook(
    FilterHook[CreateParserContextHookAction, CreateParserContextHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to create a markup
    parser instance.

    # Example

    The code below implements a custom filter function that adds new block pattern
    to the parser:

    ```python
    from misago.parser.parser import Parser

    from .patterns import PluginPattern


    @create_parser_hook.append_filter
    def register_custom_pattern(
        action: CreateParserContextHookAction, *, block_patterns, **kwargs
    ) -> dict:
        block_patterns.append(PluginPattern)

        # Call the next function in chain
        return action(block_patterns=block_patterns, **kwargs)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CreateParserContextHookAction,
        *,
        request: HttpRequest | None = None,
        user_permissions: UserPermissionsProxy | None = None,
        settings: dict | None = None,
        cache_versions: dict | None = None,
    ) -> dict:
        return super().__call__(
            action,
            request=request,
            user_permissions=user_permissions,
            settings=settings,
            cache_versions=cache_versions,
        )


create_parser_context_hook = CreateParserContextHook()
