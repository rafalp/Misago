from typing import Callable, Protocol

from django.contrib.auth import get_user_model
from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..parser import Parser, Pattern

User = get_user_model()


class CreateParserHookAction(Protocol):
    """
    A standard Misago function used to create a markup parser instance or the
    next filter function from another plugin.

    # Arguments

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
        *,
        block_patterns: list[Pattern],
        inline_patterns: list[Pattern],
        post_processors: list[Callable[[Parser, list[dict]], list[dict]]],
        user: User | None = None,
        request: HttpRequest | None = None,
        content_type: str | None = None,
    ) -> Parser:
        ...


class CreateParserHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CreateParserHookAction`

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
        action: CreateParserHookAction,
        *,
        block_patterns: list[Pattern],
        inline_patterns: list[Pattern],
        post_processors: list[Callable[[Parser, list[dict]], list[dict]]],
        user: User | None = None,
        request: HttpRequest | None = None,
        content_type: str | None = None,
    ) -> Parser:
        ...


class CreateParserHook(FilterHook[CreateParserHookAction, CreateParserHookFilter]):
    """
    This hook wraps the standard function that Misago uses to create a markup
    parser instance.

    # Example

    The code below implements a custom filter function that adds new block pattern
    to the parser:

    ```python
    from misago.parser.parser import Parser

    from .patterns import PluginPattern


    @create_markdown_hook.append_filter
    def register_custom_pattern(
        action: CreateParserHookAction, *, block_patterns, **kwargs
    ) -> Parser:
        block_patterns.append(PluginPattern)

        # Call the next function in chain
        return action(block_patterns=block_patterns, **kwargs)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CreateParserHookAction,
        *,
        block_patterns: list[Pattern],
        inline_patterns: list[Pattern],
        post_processors: list[Callable[[Parser, list[dict]], list[dict]]],
        user: User | None = None,
        request: HttpRequest | None = None,
        content_type: str | None = None,
    ) -> Parser:
        return super().__call__(
            action,
            block_patterns=block_patterns,
            inline_patterns=inline_patterns,
            post_processors=post_processors,
            user=user,
            request=request,
            content_type=content_type,
        )


create_parser_hook = CreateParserHook()
