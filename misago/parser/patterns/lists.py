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
            if group["type"] == "list":
                ast.append(self.parse_list_group(parser, group, parents))
            elif group["type"] == "text":
                ast += parser.parse_blocks(group["text"], parents)

        return ast

    def parse_list_group(self, parser: Parser, group: dict, parents: list[str]) -> dict:
        return {
            "type": "list",
            "ordered": group["number"] is not None,
            "start": group["number"],
            "delimiter": group["delimiter"],
            "tight": True,
            "children": [
                {
                    "type": "list-item",
                    "children": parser.parse_blocks(
                        group["text"], parents + ["list", "list-item"]
                    ),
                },
            ],
        }

    def split_match_into_groups(self, match: str) -> list[dict]:
        lines = [self.parse_match_line(line) for line in match.splitlines()]

        groups: list[dict] = []
        for line in lines:
            if not groups:
                groups.append(line)
                continue

            last_group = groups[-1]
            if line["type"] == "blank" and last_group["type"] == "list":
                last_group["tight"] = False

            if line["type"] in ("text", "blank"):
                if last_group["type"] == "list":
                    last_group["text"] += "\n" + line["text"]

                if last_group["type"] == "text":
                    last_group["text"] += "\n" + line["text"]

            if line["type"] == "list":
                pass

        return groups

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
            "tight": True,
            "text": line_clean,
        }
