from ..parser import Parser, Pattern


class InlineBBCodePattern(Pattern):
    pattern_type: str
    pattern: str
    invalid_parents: list[str] | None = None

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

        if self.has_invalid_parent(parents):
            return parser.parse_inline(content, parents)

        return {
            "type": self.pattern_type,
            "children": parser.parse_inline(content, parents + [self.pattern_type]),
        }

    def has_invalid_parent(self, parents: list[str]) -> bool:
        if self.pattern_type in parents:
            return True
        if self.invalid_parents:
            for invalid_parent in self.invalid_parents:
                if invalid_parent in parents:
                    return True

        return False


class BoldBBCodePattern(InlineBBCodePattern):
    pattern_type: str = "bold-bbcode"
    pattern: str = InlineBBCodePattern.create_pattern("b")
    invalid_parents: list[str] = ["strong", "emphasis"]


class ItalicsBBCodePattern(InlineBBCodePattern):
    pattern_type: str = "italics-bbcode"
    pattern: str = InlineBBCodePattern.create_pattern("i")
    invalid_parents: list[str] = ["strong", "emphasis"]


class UnderlineBBCodePattern(InlineBBCodePattern):
    pattern_type: str = "underline-bbcode"
    pattern: str = InlineBBCodePattern.create_pattern("u")


class StrikethroughBBCodePattern(InlineBBCodePattern):
    pattern_type: str = "strikethrough-bbcode"
    pattern: str = InlineBBCodePattern.create_pattern("s")
    invalid_parents: list[str] = ["strikethrough"]


class SuperscriptBBCodePattern(InlineBBCodePattern):
    pattern_type: str = "superscript-bbcode"
    pattern: str = InlineBBCodePattern.create_pattern("sup")
    invalid_parents: list[str] = ["subscript-bbcode"]


class SubscriptBBCodePattern(InlineBBCodePattern):
    pattern_type: str = "subscript-bbcode"
    pattern: str = InlineBBCodePattern.create_pattern("sub")
    invalid_parents: list[str] = ["superscript-bbcode"]
