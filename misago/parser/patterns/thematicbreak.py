from ..parser import Parser, Pattern


class ThematicBreakMarkdown(Pattern):
    pattern_type: str = "thematic-break"
    pattern: str = (
        r"(\n|^) {0,3}((-\s*-\s*-(\s*-)*)|(_\s*_\s*_(\s*_)*)|(\*\s*\*\s*\*(\s*\*)*))\s*(\n|$)"
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
