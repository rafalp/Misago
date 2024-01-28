from ..parser import Parser
from .block import BlockPostProcessor


class SpoilerBBCodePostProcessor(BlockPostProcessor):
    opening_type = "spoiler-bbcode-open"
    closing_type = "spoiler-bbcode-close"

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
            "type": "spoiler-bbcode",
            "summary": opening_block["summary"],
            "children": self(parser, children),
        }
