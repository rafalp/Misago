import re
from textwrap import dedent

from ..parser import Parser, Pattern


def dedent_and_strip(text: str) -> str:
    lines = text.strip("\n").splitlines()
    min_spaces = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    return "\n".join(line[min_spaces:] if line.strip() else "" for line in lines)


def unescape(parser: Parser, code: str) -> str:
    for placeholder, value in parser.string_placeholders.items():
        if placeholder in code:
            code = code.replace(placeholder, value)

    for value, placeholder in parser.character_placeholders.items():
        if placeholder in code:
            code = code.replace(placeholder, "\\" + value)

    return code


class FencedCodeMarkdown(Pattern):
    pattern_type: str = "code"
    pattern: str = (
        r"(^|\n)"
        r"("
        r"((?P<codedelimiter>```+).*(\n.*)*?\n(?P=codedelimiter) *(?=\n|$))"
        r"|((?P<codedelimiter2>~~~+).*(\n.*)*?\n(?P=codedelimiter2) *(?=\n|$))"
        r"|(```.*(\n.*)*)"
        r"|(~~~.*(\n.*)*)"
        r")"
    )

    def parse(self, parser: Parser, match: str, parents: list[str]) -> dict:
        match = match.lstrip()

        delimiter = match[0]
        delimiter_len = len(match) - len(match.lstrip(delimiter))

        match = match[delimiter_len:]
        if match.rstrip().endswith(delimiter * delimiter_len):
            match = match.rstrip()[: -1 * delimiter_len]

        syntax = parser.unescape(match[: match.index("\n")].strip())
        code = unescape(parser, match[match.index("\n") :]).strip("\n")
        code = "\n".join(line if line.strip() else "" for line in code.splitlines())

        return {
            "type": self.pattern_type,
            "syntax": syntax or None,
            "code": code,
        }


class IndentedCodeMarkdown(Pattern):
    pattern_type = "code-indented"
    pattern: str = r"(^|\n) {4}.+" r"((\n *)*\n+ {4}.+)*"

    def parse(self, parser: Parser, match: str, parents: list[str]) -> dict:
        return {
            "type": self.pattern_type,
            "syntax": None,
            "code": dedent_and_strip(unescape(parser, match)),
        }


class CodeBBCode(Pattern):
    pattern_type: str = "code-bbcode"
    pattern: str = r"\[code(=.+)?\]((.|\n)*?)\[\/code\]"
    contents_pattern = re.compile(
        r"\[code(=(?P<syntax>(.+)))?\](?P<code>((.|\n)*?))\[\/code\]",
        re.IGNORECASE,
    )

    def parse(self, parser: Parser, match: str, parents: list[str]) -> dict:
        contents = self.contents_pattern.match(match.strip())
        syntax = parser.unescape((contents.group("syntax") or "").strip("\"'")).strip()

        return {
            "type": self.pattern_type,
            "syntax": syntax or None,
            "code": unescape(
                parser,
                dedent(contents.group("code").lstrip("\n").rstrip()).rstrip(),
            ),
        }


class InlineCodeMarkdown(Pattern):
    pattern_type: str = "code-inline"
    pattern: str = r"`.+?(\n.+?)*?`"
    linebreaks_pattern = re.compile(r"\n+")

    def parse(self, parser: Parser, match: str, parents: list[str]) -> dict:
        code = parser.string_placeholders.pop(match[1:-1])

        for value, placeholder in parser.character_placeholders.items():
            if placeholder in code:
                replacement = "`" if value == "`" else "\\" + value
                code = code.replace(placeholder, replacement)

        return {
            "type": self.pattern_type,
            "code": code.replace("\n", " "),
        }
