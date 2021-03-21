from typing import Optional

from ..hooks import convert_rich_text_block_to_html_hook, convert_rich_text_to_html_hook
from ..types import GraphQLContext, RichText, RichTextBlock
from .highlight import highlight_code

__all__ = ["convert_rich_text_block_to_html", "convert_rich_text_to_html"]


def convert_rich_text_to_html(context: GraphQLContext, rich_text: RichText) -> str:
    return convert_rich_text_to_html_hook.call_action(
        convert_rich_text_to_html_action, context, rich_text
    )


def convert_rich_text_to_html_action(
    context: GraphQLContext, rich_text: RichText
) -> str:
    html = []
    for node in rich_text:
        node_html = convert_rich_text_block_to_html(context, node)
        if node_html:
            html.append(node_html)
    return "\n".join(html)


def convert_rich_text_block_to_html(
    context: GraphQLContext, block: RichTextBlock
) -> Optional[str]:
    return convert_rich_text_block_to_html_hook.call_action(
        convert_rich_text_block_to_html_action, context, block
    )


HEADINGS = ("h1", "h2", "h3", "h4", "h5", "h6")


def convert_rich_text_block_to_html_action(
    context: GraphQLContext, block: RichTextBlock
) -> Optional[str]:
    # pylint: disable=too-many-return-statements
    if block["type"] == "code":
        return "<pre><code>%s</code></pre>" % highlight_code(
            block["text"], block["syntax"]
        )

    if block["type"] == "f":
        return block["text"]

    if block["type"] == "hr":
        return "<hr/>"

    if block["type"] == "li":
        return "<li>%s</li>" % convert_rich_text_to_html(context, block["children"])

    if block["type"] == "list":
        element = "ol" if block["ordered"] else "ul"
        return "<%(element)s>%(children)s</%(element)s>" % {
            "element": element,
            "children": convert_rich_text_to_html(context, block["children"]),
        }

    if block["type"] == "p":
        return f"<p>{block['text']}</p>"

    if block["type"] == "quote":
        return "<blockquote>%s</blockquote>" % convert_rich_text_to_html(
            context, block["children"]
        )

    if block["type"] == "spoiler":
        return "<blockquote>%s</blockquote>" % convert_rich_text_to_html(
            context, block["children"]
        )

    if block["type"] in HEADINGS:
        return f"<div class=\"{block['type']}\">{block['text']}</div>"

    return None
