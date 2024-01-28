import re
from textwrap import dedent

from ..parser import Parser, Pattern

BLOCK_START = r"(\n|^)"
BLOCK_END = r"(\s+)?($|\n)"
CODE_FENCE = r"(```(.+)?\n(.|\n)+?\n```)"
CODE_FENCE_ALT = r"(~~~(.+)?\n(.|\n)+?\n~~~)"

CODE_FENCE_CONTENTS = re.compile(r"(?P<syntax>(.+))?\n(?P<code>(.|\n)+)\n")


class FencedCodeMarkdown(Pattern):
    pattern_type: str = "code"
    pattern: str = BLOCK_START + f"{CODE_FENCE}|{CODE_FENCE_ALT}" + BLOCK_END

    def parse(self, parser: Parser, match: str, parents: list[str]) -> dict:
        contents = CODE_FENCE_CONTENTS.match(match.strip()[3:-3])
        syntax = str(contents.group("syntax") or "").strip()
        if syntax:
            syntax = parser.reverse_reservations(syntax)

        return {
            "type": self.pattern_type,
            "syntax": syntax or None,
            "code": parser.reverse_reservations(
                contents.group("code").lstrip("\n").rstrip(),
            ),
        }


class IndentedCodeMarkdown(Pattern):
    pattern_type = "code-indented"
    pattern: str = r"(\n|^) {4}.+(\n {4}.+)*"

    def parse(self, parser: Parser, match: str, parents: list[str]) -> dict:
        return {
            "type": self.pattern_type,
            "syntax": None,
            "code": parser.reverse_reservations(
                dedent(match.strip("\n")).strip(),
            ),
        }


CODE_BBCODE_PATTERN = r"\[code(=.+)?\]((.|\n)*?)\[\/code\]"
CODE_BBCODE_CONTENTS = re.compile(
    r"\[code(=(?P<syntax>(.+)))?\](?P<code>((.|\n)*?))\[\/code\]", re.IGNORECASE
)


class CodeBBCode(Pattern):
    pattern_type: str = "code-bbcode"
    pattern: str = CODE_BBCODE_PATTERN

    def parse(self, parser: Parser, match: str, parents: list[str]) -> dict:
        contents = CODE_BBCODE_CONTENTS.match(match.strip())
        syntax = str(contents.group("syntax") or "").strip("\"' ")
        if syntax:
            syntax = parser.reverse_reservations(syntax)

        return {
            "type": self.pattern_type,
            "syntax": syntax or None,
            "code": parser.reverse_reservations(
                dedent(contents.group("code").rstrip()).strip(),
            ),
        }


class InlineCodeMarkdown(Pattern):
    pattern_type: str = "code-inline"
    pattern: str = r"(?<!\\)`(.|\n)*?(?<!\\)`"
    linebreaks_pattern = re.compile(r"\n+")

    def parse(self, parser: Parser, match: str, parents: list[str]) -> dict:
        code = match.strip("`")
        if "\n" in code:
            code = self.linebreaks_pattern.sub(" ", code)

        return {
            "type": self.pattern_type,
            "code": code,
        }
