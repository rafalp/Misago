from typing import Optional

from ..hooks import convert_rich_text_block_to_html_hook, convert_rich_text_to_html_hook
from ..types import GraphQLContext, RichText, RichTextBlock


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


def convert_rich_text_block_to_html_action(
    context: GraphQLContext, block: RichTextBlock
) -> Optional[str]:
    if block["type"] == "p":
        return f"<p>{block['text']}</p>"

    return None
