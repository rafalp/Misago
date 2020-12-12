from html import escape
from typing import Any, List, Optional, cast

from mistune import AstRenderer, BlockParser, InlineParser, Markdown

from ..hooks import create_markdown_hook
from ..types import GraphQLContext, MarkdownPlugin, RichText, RichTextBlock
from ..utils.strings import get_random_string
from .markdown import html_markdown


async def parse_markup(context: GraphQLContext, markup: str) -> RichText:
    markdown = create_markdown(context)
    ast = markdown(markup)

    return convert_ast_to_richtext(context, ast)


def create_markdown(context: GraphQLContext) -> Markdown:
    return create_markdown_hook.call_action(
        create_markdown_action, BlockParser(), InlineParser(AstRenderer()), [], context,
    )


def create_markdown_action(
    block: BlockParser,
    inline: InlineParser,
    plugins: List[MarkdownPlugin],
    context: GraphQLContext,
) -> Markdown:
    return Markdown(None, block, inline, plugins)


def convert_ast_to_richtext(context: GraphQLContext, ast: List[dict]) -> RichText:
    rich_text = []
    for node in ast:
        richtext_block = convert_block_ast_to_richtext(context, node)
        if richtext_block:
            rich_text.append(richtext_block)

    return cast(RichText, rich_text)


def convert_block_ast_to_richtext(
    context: GraphQLContext, ast: dict
) -> Optional[RichTextBlock]:
    if ast["type"] == "paragraph":
        return {
            "id": get_block_id(),
            "type": "p",
            "text": convert_inline_ast_to_text(context, ast["children"]),
        }

    return None


def convert_inline_ast_to_text(context: GraphQLContext, ast: Any) -> str:
    nodes = []
    for node in ast:
        if node["type"] in ("text", "inline_html"):
            nodes.append(escape(node["text"]))

        if node["type"] == "link":
            nodes.append(
                '<a href="%s" rel="nofollow">%s</a>'
                % (
                    escape(node["link"]),
                    convert_inline_ast_to_text(context, node["children"]),
                )
            )

        if node["type"] == "emphasis":
            nodes.append(
                "<em>%s</em>" % convert_inline_ast_to_text(context, node["children"])
            )

        if node["type"] == "strong":
            nodes.append(
                "<strong>%s</strong>"
                % convert_inline_ast_to_text(context, node["children"])
            )

    return "".join(nodes)


def get_block_id() -> str:
    return get_random_string(6)


def markup_as_html(markup: str) -> str:
    return html_markdown(markup)
