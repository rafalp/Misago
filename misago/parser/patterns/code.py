import re

from ..parser import Parser, Pattern

BLOCK_START = r"(\n|^)"
BLOCK_END = r"(\s+)?($|\n)"
CODE_FENCE = r"(```(.+)?\n(.|\n)+?\n```)"
CODE_FENCE_ALT = r"(~~~(.+)?\n(.|\n)+?\n~~~)"

CODE_FENCE_CONTENTS = re.compile(r"(?P<syntax>(.+))?\n(?P<code>(.|\n)+)\n")


def dedent(text: str) -> str:
    lines = text.splitlines()
    min_spaces = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    return "\n".join(line[min_spaces:] if line.strip() else "" for line in lines)


class FencedCodeMarkdown(Pattern):
    pattern_type: str = "code"
    pattern: str = BLOCK_START + f"{CODE_FENCE}|{CODE_FENCE_ALT}" + BLOCK_END

    def parse(self, parser: Parser, match: str, parents: list[str]) -> dict:
        contents = CODE_FENCE_CONTENTS.match(match.strip()[3:-3])
        syntax = parser.unescape(str(contents.group("syntax") or "").strip())

        return {
            "type": self.pattern_type,
            "syntax": syntax or None,
            "code": parser.unescape(
                contents.group("code").lstrip("\n").rstrip(),
            ),
        }


class IndentedCodeMarkdown(Pattern):
    pattern_type = "code-indented"
    pattern: str = r"(\n|^) {4}.+(\n+ {4}.+)*"

    def parse(self, parser: Parser, match: str, parents: list[str]) -> dict:
        return {
            "type": self.pattern_type,
            "syntax": None,
            "code": parser.unescape(
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
        syntax = parser.unescape(str(contents.group("syntax") or "").strip("\"' "))

        return {
            "type": self.pattern_type,
            "syntax": syntax or None,
            "code": parser.unescape(
                dedent(contents.group("code").rstrip()).strip(),
            ),
        }


class InlineCodeMarkdown(Pattern):
    pattern_type: str = "code-inline"
    pattern: str = r"`.+?(\n.+?)*?`"
    linebreaks_pattern = re.compile(r"\n+")

    def parse(self, parser: Parser, match: str, parents: list[str]) -> dict:
        code = parser.placeholders.pop(match[1:-1])[1:-1]

        for value, placeholder in parser.placeholders.items():
            if placeholder in code:
                replacement = "`" if value == "`" else "\\" + value
                code = code.replace(placeholder, replacement)

        return {
            "type": self.pattern_type,
            "code": code.replace("\n", " "),
        }
