from ..parser import Parser, Pattern


class Escape(Pattern):
    pattern_type: str = "escape"
    pattern: str = r"\\(_|[^\w\s])"

    def parse(
        self, parser: Parser, match: str, parents: list[str]
    ) -> dict | list[dict]:
        return {"type": self.pattern_type, "sign": match[1:]}
