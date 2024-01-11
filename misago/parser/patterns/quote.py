import re
from textwrap import dedent

from ..parser import Parser, Pattern


class QuoteBBCodeOpen(Pattern):
    pattern: str = r"\[quote\]"

    def parse(self, parser: Parser, match: str) -> dict:
        return {
            "type": "quote-bbcode-open",
        }


class QuoteBBCodeClose(Pattern):
    pattern: str = r"\[\/quote\]"

    def parse(self, parser: Parser, match: str) -> dict:
        return {
            "type": "quote-bbcode-close",
        }
