from ..parents import has_invalid_parent
from ..parser import Parser, Pattern


class InlineBBCodePattern(Pattern):
    pattern_type: str
    pattern: str
    invalid_parents: set[str] | None = None

    @staticmethod
    def create_pattern(bbcode: str) -> str:
        return r"\[" + bbcode + r"\](.|\n)*?\[\/" + bbcode + r"\]"

    def parse(
        self, parser: Parser, match: str, parents: list[str]
    ) -> dict | list[dict]:
        content_start = match.find("]") + 1
        content_end = match.rfind("[")
        content = match[content_start:content_end]

        if not content.strip():
            return []

        if has_invalid_parent(self.invalid_parents, parents):
            return parser.parse_inline(content, parents)

        return {
            "type": self.pattern_type,
            "children": parser.parse_inline(content, parents + [self.pattern_type]),
        }


class BoldBBCode(InlineBBCodePattern):
    pattern_type: str = "bold-bbcode"
    pattern: str = InlineBBCodePattern.create_pattern("b")
    invalid_parents: set[str] = {pattern_type, "strong", "strong-underline"}


class ItalicsBBCode(InlineBBCodePattern):
    pattern_type: str = "italics-bbcode"
    pattern: str = InlineBBCodePattern.create_pattern("i")
    invalid_parents: set[str] = {pattern_type, "emphasis", "emphasis-underline"}


class UnderlineBBCode(InlineBBCodePattern):
    pattern_type: str = "underline-bbcode"
    pattern: str = InlineBBCodePattern.create_pattern("u")
    invalid_parents: set[str] = {pattern_type}


class StrikethroughBBCode(InlineBBCodePattern):
    pattern_type: str = "strikethrough-bbcode"
    pattern: str = InlineBBCodePattern.create_pattern("s")
    invalid_parents: set[str] = {pattern_type, "strikethrough"}


class SuperscriptBBCode(InlineBBCodePattern):
    pattern_type: str = "superscript-bbcode"
    pattern: str = InlineBBCodePattern.create_pattern("sup")
    invalid_parents: set[str] = {pattern_type, "subscript-bbcode"}


class SubscriptBBCode(InlineBBCodePattern):
    pattern_type: str = "subscript-bbcode"
    pattern: str = InlineBBCodePattern.create_pattern("sub")
    invalid_parents: set[str] = {pattern_type, "superscript-bbcode"}
