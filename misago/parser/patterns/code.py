import re
from textwrap import dedent

from ..parser import Parser, Pattern

BLOCK_START = r"(\n|^)"
BLOCK_END = r"(\s+)?$|\n"
CODE_FENCE = r"(```(.+)?\n(.|\n)+\n```)"
CODE_FENCE_ALT = r"(~~~(.+)?\n(.|\n)+\n~~~)"

CODE_FENCE_CONTENTS = re.compile(r"(?P<syntax>(.+))?\n(?P<code>(.|\n)+)\n")


class FencedCodeMarkdown(Pattern):
    pattern: str = BLOCK_START + f"({CODE_FENCE}|{CODE_FENCE_ALT})" + BLOCK_END

    def parse(self, parser: Parser, match: str) -> dict:
        contents = CODE_FENCE_CONTENTS.match(match.strip()[3:-3])
        return {
            "type": "code",
            "syntax": str(contents.group("syntax") or "").strip() or None,
            "code": dedent(contents.group("code").rstrip()).strip(),
        }
