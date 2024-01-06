from typing import Callable

from django.contrib.auth import get_user_model
from django.http import HttpRequest
from mistune import BlockParser, InlineParser, Markdown
from mistune.plugins.formatting import strikethrough
from mistune.plugins.url import url as url_plugin

from .hooks import create_markdown_hook

User = get_user_model()


def create_markdown(
    *,
    user: User | None = None,
    request: HttpRequest | None = None,
    content_type: str | None = None,
    enable_mentions: bool = True,
    enable_media: bool = True,
    enable_blocks: bool = True,
) -> Markdown:
    plugins = [
        url_plugin,
        strikethrough,
    ]

    block_parser = BlockParser()
    inline_parser = InlineParser()

    # Remove HTML support
    block_parser.specification.pop("block_html")
    block_parser.specification.pop("raw_html")
    block_parser.rules.remove("raw_html")

    inline_parser.specification.pop("inline_html")
    inline_parser.rules.remove("inline_html")

    # Remove ref link
    block_parser.specification.pop("ref_link")
    block_parser.rules.remove("ref_link")

    if not enable_blocks:
        block_parser.specification.pop("atx_heading")
        block_parser.specification.pop("setex_heading")
        block_parser.specification.pop("fenced_code")
        block_parser.specification.pop("indent_code")
        block_parser.specification.pop("thematic_break")
        block_parser.specification.pop("block_quote")
        block_parser.specification.pop("list")
        block_parser.rules.remove("fenced_code")
        block_parser.rules.remove("indent_code")
        block_parser.rules.remove("atx_heading")
        block_parser.rules.remove("setex_heading")
        block_parser.rules.remove("thematic_break")
        block_parser.rules.remove("block_quote")
        block_parser.rules.remove("list")

    return create_markdown_hook(
        _create_markdown_action,
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


def _create_markdown_action(
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
    return Markdown(None, block_parser, inline_parser, plugins)
