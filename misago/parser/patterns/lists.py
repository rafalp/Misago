import re
from textwrap import dedent

from ..parser import Parser, Pattern

LIST_PATTERN = (
    r"(^|\n)"
    r" {0,3}("
    r"(-|\+|\*|([0-9]{1,9}(\.|\))))"
    r"((( .*)?((\n.+)|(\n+  +.*))+)|( .*))"
    r")(?=\n|$)"
)

ListItem = tuple[int, str, list[dict]]


class ListMarkdown(Pattern):
    pattern_type: str = "list"
    pattern: str = LIST_PATTERN

    item_start_pattern = re.compile(r"^ *(-|\+|\*|([0-9]{1,9}(\.|\))))( .*)?$")
    delimiters: str = "-+*"

    def parse(self, parser: Parser, match: str, parents: list[str]) -> list[dict]:
        groups = self.split_match_into_groups(match)

        ast: list[dict] = []
        for group in groups:
            ast.append(
                {
                    "type": "list",
                    "ordered": group["number"] is not None,
                    "start": group["number"],
                    "delimiter": group["delimiter"],
                    "tight": True,
                    "children": [
                        {
                            "type": "list-item",
                            "children": [
                                {
                                    "type": "paragraph",
                                    "children": [
                                        {"type": "text", "text": group["text"].strip()},
                                    ],
                                },
                            ],
                        },
                    ],
                }
            )

        return ast

    def split_match_into_groups(self, match: str) -> list[dict]:
        lines = [self.parse_match_line(line) for line in match.splitlines()]
        return lines

    def parse_match_line(self, line: str) -> dict:
        if self.item_start_pattern.match(line):
            return self.parse_list_item_line(line)

        if not line.strip():
            return {"type": "blank", "text": line}

        return {
            "type": "text",
            "indent": len(line) - len(line.lstrip()),
            "text": line,
        }

    def parse_list_item_line(self, line: str) -> dict | None:
        line_clean = line.lstrip()
        indent = len(line) - len(line_clean)

        if line_clean[0] in self.delimiters:
            number = None
            delimiter = line_clean[0]
            start = 1 + len(line_clean[1:]) - len(line_clean[1:].lstrip())
            line_clean = line_clean[1:]
        else:
            if ")" in line_clean and "." in line_clean:
                delimiter_position = min(line_clean.index(")"), line_clean.index("."))
            elif ")" in line_clean:
                delimiter_position = line_clean.index(")")
            else:
                delimiter_position = line_clean.index(".")

            number = int(line_clean[:delimiter_position])
            delimiter = line_clean[delimiter_position]
            line_clean = line_clean[delimiter_position + 1 :]
            start = delimiter_position + 1 + len(line_clean) - len(line_clean.lstrip())

        return {
            "type": "list",
            "indent": indent,
            "number": number,
            "delimiter": delimiter,
            "start": indent + start,
            "text": line_clean,
        }
