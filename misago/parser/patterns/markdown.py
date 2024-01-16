from ..parser import Parser, Pattern


class InlineMarkdownPattern(Pattern):
    pattern_type: str
    pattern: str
    pattern_length: int
    invalid_parents: list[str] | None = None

    def parse(
        self, parser: Parser, match: str, parents: list[str]
    ) -> dict | list[dict]:
        content = match[self.pattern_length : self.pattern_length * -1]
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


class EmphasisUnderscoreMarkdown(InlineMarkdownPattern):
    pattern_type: str = "emphasis-underscore"
    pattern: str = r"(?<!\w)_.+(\n.+)*?_(?!\w)"
    pattern_length: int = 1
    invalid_parents: list[str] = ["emphasis"]


class StrongUnderscoreMarkdown(InlineMarkdownPattern):
    pattern_type: str = "strong-underscore"
    pattern: str = r"(?<!\w)__.+(\n.+)*?__(?!\w)"
    pattern_length: int = 2
    invalid_parents: list[str] = ["strong"]


class EmphasisMarkdown(InlineMarkdownPattern):
    pattern_type: str = "emphasis"
    pattern: str = r"*.+(\n.+)*?*"
    pattern_length: int = 1
    invalid_parents: list[str] = ["emphasis-underscore"]


class StrongMarkdown(InlineMarkdownPattern):
    pattern_type: str = "strong"
    pattern: str = r"**.+(\n.+)*?**"
    pattern_length: int = 2
    invalid_parents: list[str] = ["strong-underscore"]


class StrikethroughMarkdown(InlineMarkdownPattern):
    pattern_type: str = "strikethrough"
    pattern: str = r"~~.+(\n.+)*?~~"
    pattern_length: int = 2
