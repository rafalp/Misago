import re

from ..parser import Parser, Pattern

ESCAPE = r"\\(_|[^\w\s])"


class Escape(Pattern):
    pattern_type: str = "escape"
    pattern: str = ESCAPE

    def parse(
        self, parser: Parser, match: str, parents: list[str]
    ) -> dict | list[dict]:
        return {"type": self.pattern_type, "character": match[1:]}


ESCAPE_RE = re.compile(ESCAPE)


def unescape_markup(value: str) -> str:
    return ESCAPE_RE.sub("\\1", value)
