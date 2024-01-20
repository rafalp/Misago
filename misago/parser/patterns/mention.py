from ..parents import has_invalid_parent
from ..parser import Parser, Pattern
from .urls import UrlBBCode, UrlMarkdown


class Mention(Pattern):
    pattern_type: str = "mention"
    pattern: str = r"(?<!\w)@[a-zA-Z0-9-_]+"
    invalid_parents: set[str] = {UrlBBCode.pattern_type, UrlMarkdown.pattern_type}

    def parse(self, parser: Parser, match: str, parents: list[dict]) -> dict:
        if has_invalid_parent(self.invalid_parents, parents):
            return {"type": "text", "text": match}

        return {"type": self.pattern_type, "username": match[1:]}
