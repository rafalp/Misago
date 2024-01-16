from ..parser import Parser, Pattern


class AtxHeading(Pattern):
    pattern_type: str = "heading"
    pattern: str = r"(\n|^)#{1,6}.*"

    def parse(
        self, parser: Parser, match: str, parents: list[str]
    ) -> dict | list[dict]:
        content = match.strip()
        level = 0

        while content.startswith("#"):
            content = content[1:]
            level += 1

        return {
            "type": self.pattern_type,
            "level": level,
            "children": parser.parse_inline(
                content.strip(),
                parents + [self.pattern_type],
                reverse_reservations=True,
            ),
        }


class SetexHeading(Pattern):
    pattern_type: str = "heading-setex"
    pattern: str = r"(\n|^).+\n((=+)|(-+)) *(\n|$)"

    def parse(
        self, parser: Parser, match: str, parents: list[str]
    ) -> dict | list[dict]:
        content, underline = match.strip().splitlines()

        return {
            "type": self.pattern_type,
            "level": 1 if underline[0] == "=" else 2,
            "children": parser.parse_inline(
                content.strip(),
                parents + [self.pattern_type],
                reverse_reservations=True,
            ),
        }
