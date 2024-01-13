from ..parser import Parser, Pattern


class SpoilerBBCodeOpen(Pattern):
    pattern: str = r"\[spoiler(=.*?)?\]"

    def parse(self, parser: Parser, match: str) -> dict:
        summary = parser.reverse_patterns(match[8:-1].strip("\"' ="))

        return {
            "type": "spoiler-bbcode-open",
            "summary": summary or None,
        }


class SpoilerBBCodeClose(Pattern):
    pattern: str = r"\[\/spoiler\]"

    def parse(self, parser: Parser, match: str) -> dict:
        return {
            "type": "spoiler-bbcode-close",
        }
