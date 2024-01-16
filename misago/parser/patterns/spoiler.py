from ..parser import Parser, Pattern


class SpoilerBBCodeOpen(Pattern):
    pattern_type: str = "spoiler-bbcode-open"
    pattern: str = r"\[spoiler(=.*?)?\]"

    def parse(self, parser: Parser, match: str, parents: list[str]) -> dict:
        summary = parser.reverse_reservations(match[8:-1].strip("\"' ="))

        return {
            "type": self.pattern_type,
            "summary": summary or None,
        }


class SpoilerBBCodeClose(Pattern):
    pattern_type: str = "spoiler-bbcode-close"
    pattern: str = r"\[\/spoiler\]"

    def parse(self, parser: Parser, match: str, parents: list[str]) -> dict:
        return {"type": self.pattern_type}
