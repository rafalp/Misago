from ..parents import has_invalid_parent
from ..parser import Parser, Pattern


class InlineMarkdownPattern(Pattern):
    pattern_type: str
    pattern: str
    pattern_length: int
    invalid_parents: set[str] | None = None

    def parse(
        self, parser: Parser, match: str, parents: list[str]
    ) -> dict | list[dict]:
        content = match[self.pattern_length : self.pattern_length * -1]
        if not content:
            return {"type": "text", "text": match}

        if not content.strip():
            pattern = {"type": "text", "text": match[: self.pattern_length]}
            return [pattern] + parser.parse_inline(content, parents) + [pattern]

        if has_invalid_parent(self.invalid_parents, parents):
            return parser.parse_inline(content, parents)

        return {
            "type": self.pattern_type,
            "children": parser.parse_inline(content, parents + [self.pattern_type]),
        }


class EmphasisUnderscoreMarkdown(InlineMarkdownPattern):
    pattern_type: str = "emphasis-underscore"
    pattern: str = r"(?<!\w)_.+?(\n.+)*?_(?!\w)"
    pattern_length: int = 1
    invalid_parents: set[str] = {pattern_type, "emphasis"}


class StrongUnderscoreMarkdown(InlineMarkdownPattern):
    pattern_type: str = "strong-underscore"
    pattern: str = r"(?<!\w)__.*?(\n.+)*?__(?!\w)"
    pattern_length: int = 2
    invalid_parents: set[str] = {pattern_type, "strong"}


class EmphasisMarkdown(InlineMarkdownPattern):
    pattern_type: str = "emphasis"
    pattern: str = r"\*.+?(\n.+)*?\*"
    pattern_length: int = 1
    invalid_parents: set[str] = {pattern_type, "emphasis-underscore"}


class StrongMarkdown(InlineMarkdownPattern):
    pattern_type: str = "strong"
    pattern: str = r"\*\*.*?(\n.+)*?\*\*"
    pattern_length: int = 2
    invalid_parents: set[str] = {pattern_type, "strong-underscore"}


class StrikethroughMarkdown(InlineMarkdownPattern):
    pattern_type: str = "strikethrough"
    pattern: str = r"~~.+?(\n.+)*?~~"
    pattern_length: int = 2
