from ..parser import Parser, Pattern


class ThematicBreakMarkdown(Pattern):
    pattern: str = r"(\n|^) {0,3}((-\s*-\s*-(\s*-)*)|(_\s*_\s*_(\s*_)*)|(\*\s*\*\s*\*(\s*\*)*))\s*(\n|$)"

    def parse(self, parser: Parser, match: str) -> dict | list[dict]:
        return {"type": "thematic-break"}


class ThematicBreakBBCode(Pattern):
    pattern: str = r"\[hr\/?\]"

    def parse(self, parser: Parser, match: str) -> dict | list[dict]:
        return {"type": "thematic-break-bbcode"}
