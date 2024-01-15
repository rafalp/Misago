from ..parser import Parser, Pattern


class AtxHeading(Pattern):
    pattern: str = r"(\n|^)#{1,6}.*"

    def parse(self, parser: Parser, match: str) -> dict | list[dict]:
        content = match.strip()
        level = 0

        while content.startswith("#"):
            content = content[1:]
            level += 1

        return {
            "type": "heading",
            "level": level,
            "children": parser.parse_inline(content.strip()),
        }


class SetexHeading(Pattern):
    pattern: str = r"(\n|^).+\n((=+)|(-+))(\s+|$)"

    def parse(self, parser: Parser, match: str) -> dict | list[dict]:
        content, underline = match.strip().splitlines()
        return {
            "type": "heading-setex",
            "level": 1 if underline[0] == "=" else 2,
            "children": parser.parse_inline(content.strip()),
        }
