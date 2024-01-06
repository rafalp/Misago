from typing import Callable, Protocol

from django.contrib.auth import get_user_model
from django.http import HttpRequest
from mistune import BlockParser, InlineParser, Markdown

from ...plugins.hooks import FilterHook

User = get_user_model()


class CreateMarkdownHookAction(Protocol):
    """
    A standard Misago function used to create a markup parser instance or the
    next filter function from another plugin.

    # Arguments

    ## `block_parser: BlockParser`

    A `BlockParser` instance to be used by the parser.

    ## `inline_parser: InlineParser`

    An `InlineParser` instance to be used by the parser.

    ## `plugins: list[Callable[[Markdown], None]]`

    A list of `mistune` plugins.

    ## `user: User | None = None`

    A `User` instance with the parsed text's author or `None` if not provided.

    ## `request: HttpRequest | None = None`

    The request object or `None` if it was not provided.

    ## `content_type: str | None = None`

    A `str` with the name of the content type to be parsed (e.g., `post` or `signature`)
    or `None` if not provided.

    ## `enable_mentions: bool = True`

    A feature flag controlling whether user mentions should be parsed.

    ## `enable_media: bool = True`

    A feature flag controlling whether media (images or embedded media)
    should be parsed.

    ## `enable_blocks: bool = True`

    A feature flag controlling whether blocks (quotes, spoilers, lists, etc.)
    should be parsed.

    # Return value

    An instance of the `Markdown` class from the `mistune` library.
    """

    def __call__(
        self,
        *,
        block_parser: BlockParser,
        inline_parser: InlineParser,
        plugins: list[Callable[[Markdown], None]],
        user: User | None = None,
        request: HttpRequest | None = None,
        content_type: str | None = None,
        enable_mentions: bool = True,
        enable_media: bool = True,
        enable_blocks: bool = True,
    ) -> Markdown:
        ...


class CreateMarkdownHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CreateMarkdownHookAction`

    A standard Misago function used to create a markup parser instance or the
    next filter function from another plugin.

    See the [action](#action) section for details.

    ## `block_parser: BlockParser`

    A `BlockParser` instance to be used by the parser.

    ## `inline_parser: InlineParser`

    An `InlineParser` instance to be used by the parser.

    ## `plugins: list[Callable[[Markdown], None]]`

    A list of `mistune` plugins.

    ## `user: User | None = None`

    A `User` instance with the parsed text's author or `None` if not provided.

    ## `request: HttpRequest | None = None`

    The request object or `None` if it was not provided.

    ## `content_type: str | None = None`

    A `str` with the name of the content type to be parsed (e.g., `post` or `signature`)
    or `None` if not provided.

    ## `enable_mentions: bool = True`

    A feature flag controlling whether user mentions should be parsed.

    ## `enable_media: bool = True`

    A feature flag controlling whether media (images or embedded media)
    should be parsed.

    ## `enable_blocks: bool = True`

    A feature flag controlling whether blocks (quotes, spoilers, lists, etc.)
    should be parsed.

    # Return value

    An instance of the `Markdown` class from the `mistune` library.
    """

    def __call__(
        self,
        action: CreateMarkdownHookAction,
        *,
        block_parser: BlockParser,
        inline_parser: InlineParser,
        plugins: list[Callable[[Markdown], None]],
        user: User | None = None,
        request: HttpRequest | None = None,
        content_type: str | None = None,
        enable_mentions: bool = True,
        enable_media: bool = True,
        enable_blocks: bool = True,
    ) -> Markdown:
        ...


class CreateMarkdownHook(
    FilterHook[CreateMarkdownHookAction, CreateMarkdownHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to create a markup
    parser instance.

    # Example

    The code below implements a custom filter function that adds the table Mistune
    plugin to the parser:

    ```python
    from typing import Callable, Protocol

    from django.contrib.auth import get_user_model
    from django.http import HttpRequest
    from mistune import BlockParser, InlineParser, Markdown
    from mistune.plugins.table import table

    User = get_user_model()

    @create_markdown_hook.append_filter
    def register_custom_markdown_plugin(
        action: CreateMarkdownHookAction, *, plugins, **kwargs
    ) -> None:
        plugins.append(table)

        # Call the next function in chain
        return action(plugins=plugins, **kwargs)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CreateMarkdownHookAction,
        *,
        block_parser: BlockParser,
        inline_parser: InlineParser,
        plugins: list[Callable[[Markdown], None]],
        user: User | None = None,
        request: HttpRequest | None = None,
        content_type: str | None = None,
        enable_mentions: bool = True,
        enable_media: bool = True,
        enable_blocks: bool = True,
    ) -> Markdown:
        return super().__call__(
            action,
            block_parser=block_parser,
            inline_parser=inline_parser,
            plugins=plugins,
            user=user,
            request=request,
            content_type=content_type,
            enable_mentions=enable_mentions,
            enable_media=enable_media,
            enable_blocks=enable_blocks,
        )


create_markdown_hook = CreateMarkdownHook()
