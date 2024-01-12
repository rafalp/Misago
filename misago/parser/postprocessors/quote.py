from ..parser import Parser
from .block import BlockPostProcessor


class QuoteBBCodePostProcessor(BlockPostProcessor):
    opening_type = "quote-bbcode-open"
    closing_type = "quote-bbcode-close"

    def wrap_block(
        self,
        parser: Parser,
        opening_block: dict,
        closing_block: dict,
        children: list[dict],
    ) -> dict | None:
        if not children:
            return None

        return {
            "type": "quote-bbcode",
            "author": opening_block["author"],
            "post": opening_block["post"],
            "children": self(parser, children),
        }
