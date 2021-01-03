from hashlib import md5
from html import escape
from typing import List, Optional, Tuple, cast

from mistune import AstRenderer, BlockParser, InlineParser, Markdown
from mistune.plugins import plugin_strikethrough

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
from .genericblocks import restructure_generic_blocks
from .mentions import clean_mention, find_user_mentions, update_metadata_from_mentions
from .plugins import builtin_plugins
from .scanner import MisagoScanner


async def parse_markup(
    context: GraphQLContext, markup: str
) -> Tuple[RichText, ParsedMarkupMetadata]:
    cache_key = get_markup_cache_key(markup)
    if cache_key not in context:
        metadata: ParsedMarkupMetadata = {"mentions": [], "users": {}}
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
    ast = markdown_hook.call_action(markdown_action, context, markup, metadata)
    await update_markup_metadata_hook.call_action(
        update_markup_metadata_action, context, ast, metadata
    )
    return convert_ast_to_rich_text(context, ast, metadata), metadata


def markdown_action(
    context: GraphQLContext, markup: str, metadata: ParsedMarkupMetadata
) -> List[dict]:
    markdown = create_markdown(context)
    markdown = restructure_generic_blocks(markdown(markup))
    find_user_mentions(markdown, metadata)
    return markdown


def create_markdown(context: GraphQLContext) -> Markdown:
    return create_markdown_hook.call_action(
        create_markdown_action,
        context,
        BlockParser(),
        MisagoInlineParser(AstRenderer()),
        [plugin_strikethrough, *builtin_plugins],
    )


class MisagoInlineParser(InlineParser):
    scanner_cls = MisagoScanner

    def parse_std_link(self, m, state):
        if state.get("_in_link"):
            return "text", m.group(0)

        return super().parse_std_link(m, state)


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


async def update_markup_metadata_action(
    context: GraphQLContext, ast: List[dict], metadata: ParsedMarkupMetadata
):
    await update_metadata_from_mentions(metadata)


def convert_ast_to_rich_text(
    context: GraphQLContext, ast: List[dict], metadata: ParsedMarkupMetadata
) -> RichText:
    rich_text = []
    for node in ast:
        richtext_block = convert_block_ast_to_rich_text(context, node, metadata)
        if richtext_block:
            rich_text.append(richtext_block)

    return cast(RichText, rich_text)


def convert_block_ast_to_rich_text(
    context: GraphQLContext, ast: dict, metadata: ParsedMarkupMetadata
) -> Optional[RichTextBlock]:
    return convert_block_ast_to_rich_text_hook.call_action(
        convert_block_ast_to_rich_text_action, context, ast, metadata
    )


def convert_block_ast_to_rich_text_action(
    context: GraphQLContext, ast: dict, metadata: ParsedMarkupMetadata
) -> Optional[RichTextBlock]:
    # pylint: disable=too-many-return-statements
    if ast["type"] == "block_text":
        return {
            "id": get_block_id(),
            "type": "f",
            "text": convert_children_ast_to_text(context, ast["children"], metadata),
        }

    if ast["type"] == "paragraph":
        return {
            "id": get_block_id(),
            "type": "p",
            "text": convert_children_ast_to_text(context, ast["children"], metadata),
        }

    if ast["type"] == "heading":
        return {
            "id": get_block_id(),
            "type": "h%s" % ast["level"],
            "text": convert_children_ast_to_text(context, ast["children"], metadata),
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
            "author": None,
            "post": None,
            "children": convert_ast_to_rich_text(context, ast["children"], metadata),
        }

    if ast["type"] == "quote_bbcode":
        if ast["author"]:
            author = clean_mention(ast["author"])
            if author in metadata["users"]:
                user = metadata["users"][author]
                ast["author"] = {
                    "id": user.id,
                    "name": user.name,
                    "slug": user.slug,
                }
            else:
                ast["author"] = {
                    "id": None,
                    "name": ast["author"],
                    "slug": None,
                }

        return {
            "id": get_block_id(),
            "type": "quote",
            "author": ast["author"],
            "post": ast["post"],
            "children": convert_ast_to_rich_text(context, ast["children"], metadata),
        }

    if ast["type"] == "spoiler_bbcode":
        return {
            "id": get_block_id(),
            "type": "spoiler",
            "children": convert_ast_to_rich_text(context, ast["children"], metadata),
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
            "children": convert_ast_to_rich_text(context, ast["children"], metadata),
        }

    if ast["type"] == "list_item":
        return {
            "id": get_block_id(),
            "type": "li",
            "children": convert_ast_to_rich_text(context, ast["children"], metadata),
        }

    return None


def get_block_id() -> str:
    return get_random_string(6)


def convert_children_ast_to_text(
    context: GraphQLContext, ast: Optional[List[dict]], metadata: ParsedMarkupMetadata
) -> str:
    # Fail-safe for situations when `ast["children"]` is None
    if not ast:
        return ""

    # Fail-safe for situations when `ast["children"]` is str
    if isinstance(ast, str):
        return escape(ast)

    nodes = []
    for node in ast:
        text = convert_inline_ast_to_text(context, node, metadata)
        if text is not None:
            nodes.append(text)

    return "".join(nodes)


def convert_inline_ast_to_text(
    context: GraphQLContext, ast: dict, metadata: ParsedMarkupMetadata
) -> Optional[str]:
    return convert_inline_ast_to_text_hook.call_action(
        convert_inline_ast_to_text_action, context, ast, metadata
    )


def convert_inline_ast_to_text_action(
    context: GraphQLContext, ast: dict, metadata: ParsedMarkupMetadata
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

    if ast["type"] == "mention":
        mention = clean_mention(ast["mention"])
        if mention not in metadata["users"]:
            return ast["fallback"]

        user = metadata["users"][mention]
        return '<a href="/u/%s/%s/">@%s</a>' % (
            escape(user.slug),
            user.id,
            escape(user.name),
        )

    if ast["type"] == "link":
        if not ast["children"]:
            children = ast["link"]
        elif isinstance(ast["children"], str):
            children = escape(ast["children"])
        else:
            children = convert_children_ast_to_text(context, ast["children"], metadata)

        return '<a href="%s" rel="nofollow">%s</a>' % (escape(ast["link"]), children)

    if ast["type"] == "emphasis":
        return "<em>%s</em>" % convert_children_ast_to_text(
            context, ast["children"], metadata
        )

    if ast["type"] == "strong":
        return "<strong>%s</strong>" % convert_children_ast_to_text(
            context, ast["children"], metadata
        )

    if ast["type"] == "strikethrough":
        return "<del>%s</del>" % convert_children_ast_to_text(
            context, ast["children"], metadata
        )

    if ast["type"] == "bold":
        return "<b>%s</b>" % convert_children_ast_to_text(
            context, ast["children"], metadata
        )

    if ast["type"] == "italic":
        return "<i>%s</i>" % convert_children_ast_to_text(
            context, ast["children"], metadata
        )

    if ast["type"] == "underline":
        return "<u>%s</u>" % convert_children_ast_to_text(
            context, ast["children"], metadata
        )

    if ast["type"] == "subscript":
        return "<sub>%s</sub>" % convert_children_ast_to_text(
            context, ast["children"], metadata
        )

    if ast["type"] == "superscript":
        return "<sup>%s</sup>" % convert_children_ast_to_text(
            context, ast["children"], metadata
        )

    return None
