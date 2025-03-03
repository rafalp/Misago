from ..parser import Parser, Pattern


class ThematicBreakMarkdown(Pattern):
    pattern_type: str = "thematic-break"
    pattern: str = (
        r"(\n|^)"
        r" {0,3}"
        r"("
        r"(- *- *-( *-)*)"
        r"|(_ *_ *_( *_)*)"
        r"|(\* *\* *\*( *\*)*)"
        r") *(\n|$)"
    )

    def parse(
        self, parser: Parser, match: str, parents: list[str]
    ) -> dict | list[dict]:
        return {"type": self.pattern_type}


class ThematicBreakBBCode(Pattern):
    pattern_type: str = "thematic-break-bbcode"
    pattern: str = r"\[hr\/?\]"

    def parse(
        self, parser: Parser, match: str, parents: list[str]
    ) -> dict | list[dict]:
        return {"type": self.pattern_type}
