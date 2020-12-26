from hashlib import md5
from html import escape
from typing import List, Optional, Tuple, cast

from mistune import AstRenderer, BlockParser, InlineParser, Markdown
from mistune.plugins import plugin_strikethrough, plugin_url

from ..hooks import (
    convert_block_ast_to_rich_text_hook,
    convert_inline_ast_to_text_hook,
    create_markdown_hook,
    markdown_hook,
    parse_markup_hook,
    update_markup_metadata_hook,
)
from ..types import (
    GraphQLContext,
    ParsedMarkupMetadata,
    MarkdownPlugin,
    RichText,
    RichTextBlock,
)
from ..utils.strings import get_random_string
from .plugins import plugin_hard_break, plugin_short_image


async def parse_markup(
    context: GraphQLContext, markup: str
) -> Tuple[RichText, ParsedMarkupMetadata]:
    cache_key = get_markup_cache_key(markup)
    if cache_key not in context:
        metadata: ParsedMarkupMetadata = {}
        context[cache_key] = await parse_markup_hook.call_action(
            parse_markup_action, context, markup, metadata
        )

    return context[cache_key]


def get_markup_cache_key(markup: str) -> str:
    markup_clean = markup.strip().encode("utf-8")
    markup_hash = md5(markup_clean).hexdigest()
    return f"markup_{markup_hash}"


async def parse_markup_action(
    context: GraphQLContext, markup: str, metadata: ParsedMarkupMetadata
) -> Tuple[RichText, ParsedMarkupMetadata]:
    ast = markdown_hook.call_action(markdown_action, context, markup)
    await update_markup_metadata_hook.call_action(context, ast, metadata)
    return convert_ast_to_rich_text(context, ast), metadata


def markdown_action(context: GraphQLContext, markup: str) -> List[dict]:
    markdown = create_markdown(context)
    return markdown(markup)


def create_markdown(context: GraphQLContext) -> Markdown:
    return create_markdown_hook.call_action(
        create_markdown_action,
        context,
        BlockParser(),
        InlineParser(AstRenderer()),
        [plugin_strikethrough, plugin_url, plugin_hard_break, plugin_short_image],
    )


def create_markdown_action(
    context: GraphQLContext,
    block: BlockParser,
    inline: InlineParser,
    plugins: List[MarkdownPlugin],
) -> Markdown:
    markdown = Markdown(None, block, inline, plugins)
    markdown.inline.rules.remove("ref_link")
    markdown.inline.rules.remove("ref_link2")
    return markdown


def convert_ast_to_rich_text(context: GraphQLContext, ast: List[dict]) -> RichText:
    rich_text = []
    for node in ast:
        richtext_block = convert_block_ast_to_rich_text(context, node)
        if richtext_block:
            rich_text.append(richtext_block)

    return cast(RichText, rich_text)


def convert_block_ast_to_rich_text(
    context: GraphQLContext, ast: dict
) -> Optional[RichTextBlock]:
    return convert_block_ast_to_rich_text_hook.call_action(
        convert_block_ast_to_rich_text_action, context, ast,
    )


def convert_block_ast_to_rich_text_action(
    context: GraphQLContext, ast: dict
) -> Optional[RichTextBlock]:
    # pylint: disable=too-many-return-statements
    if ast["type"] == "block_text":
        return {
            "id": get_block_id(),
            "type": "f",
            "text": convert_children_ast_to_text(context, ast["children"]),
        }

    if ast["type"] == "paragraph":
        return {
            "id": get_block_id(),
            "type": "p",
            "text": convert_children_ast_to_text(context, ast["children"]),
        }

    if ast["type"] == "heading":
        return {
            "id": get_block_id(),
            "type": "h%s" % ast["level"],
            "text": convert_children_ast_to_text(context, ast["children"]),
        }

    if ast["type"] == "block_code":
        return {
            "id": get_block_id(),
            "type": "code",
            "syntax": ast["info"],
            "text": escape(ast["text"]),
        }

    if ast["type"] == "block_quote":
        return {
            "id": get_block_id(),
            "type": "quote",
            "children": convert_ast_to_rich_text(context, ast["children"]),
        }

    if ast["type"] == "thematic_break":
        return {
            "id": get_block_id(),
            "type": "hr",
        }

    if ast["type"] == "list":
        return {
            "id": get_block_id(),
            "type": "list",
            "ordered": ast["ordered"],
            "children": convert_ast_to_rich_text(context, ast["children"]),
        }

    if ast["type"] == "list_item":
        return {
            "id": get_block_id(),
            "type": "li",
            "children": convert_ast_to_rich_text(context, ast["children"]),
        }

    return None


def get_block_id() -> str:
    return get_random_string(6)


def convert_children_ast_to_text(
    context: GraphQLContext, ast: Optional[List[dict]]
) -> str:
    # Fail-safe for situations when `ast["children"]` is None
    if not ast:
        return ""

    # Fail-safe for situations when `ast["children"]` is str
    if isinstance(ast, str):
        return escape(ast)

    nodes = []
    for node in ast:
        text = convert_inline_ast_to_text(context, node)
        if text is not None:
            nodes.append(text)

    return "".join(nodes)


def convert_inline_ast_to_text(context: GraphQLContext, ast: dict) -> Optional[str]:
    return convert_inline_ast_to_text_hook.call_action(
        convert_inline_ast_to_text_action, context, ast
    )


def convert_inline_ast_to_text_action(
    context: GraphQLContext, ast: dict
) -> Optional[str]:
    # pylint: disable=too-many-return-statements
    if ast["type"] == "linebreak":
        return "<br/>"

    if ast["type"] in ("text", "inline_html"):
        return escape(ast["text"])

    if ast["type"] == "codespan":
        return "<code>%s</code>" % escape(ast["text"])

    if ast["type"] == "image":
        return '<img src="%s" alt="%s" />' % (
            escape(ast["src"]),
            escape(ast["alt"] or ""),
        )

    if ast["type"] == "link":
        if not ast["children"]:
            children = ast["link"]
        elif isinstance(ast["children"], str):
            children = escape(ast["children"])
        else:
            children = convert_children_ast_to_text(context, ast["children"])

        return '<a href="%s" rel="nofollow">%s</a>' % (escape(ast["link"]), children)

    if ast["type"] == "emphasis":
        return "<em>%s</em>" % convert_children_ast_to_text(context, ast["children"])

    if ast["type"] == "strong":
        return "<strong>%s</strong>" % convert_children_ast_to_text(
            context, ast["children"]
        )

    if ast["type"] == "strikethrough":
        return "<del>%s</del>" % convert_children_ast_to_text(context, ast["children"])

    return None
