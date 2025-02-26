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
        blocks = self.split_match_into_blocks(match)

        ast: list[dict] = []
        for block in blocks:
            if block["type"] == "list":
                ast.append(self.parse_list_block(parser, block, parents))
            elif block["type"] == "text":
                ast += parser.parse_blocks(block["text"], parents)

        return ast

    def parse_list_block(self, parser: Parser, block: dict, parents: list[str]) -> dict:
        return {
            "type": "list",
            "ordered": block["number"] is not None,
            "start": block["number"],
            "delimiter": block["delimiter"],
            "tight": True,
            "children": [
                {
                    "type": "list-item",
                    "children": parser.parse_blocks(
                        child, parents + ["list", "list-item"]
                    ),
                }
                for child in block["children"]
            ],
        }

    def split_match_into_blocks(self, match: str) -> list[dict]:
        lines = self.split_match_into_lines(match)

        blocks: list[dict] = []
        last_line = None

        for line in lines:
            if not blocks:
                blocks.append(line)
                last_line = line
                continue

            last_block = blocks[-1]
            if line["type"] == "list":
                if last_block["type"] == "text" or (
                    last_block["type"] == "list"
                    and line["indent"] <= last_block["start"]
                ):
                    blocks.append(line)
                else:
                    text = "\n" + ((line["indent"] - last_block["start"]) * " ")
                    if last_block["number"] is not None:
                        text += str(last_block["number"])
                    text += str(last_block["delimiter"])
                    text += line["text"]

                    last_block["text"] += text

            elif line["type"] == "blank":
                if last_block["type"] == "list":
                    last_block["tight"] = False
                last_block["text"] += "\n" + line["text"]

            elif line["type"] == "text":
                if last_block["type"] == "list":
                    if last_line["type"] == "blank":
                        if line["indent"] >= last_block["start"]:
                            last_block["text"] += (
                                "\n" + line["text"][last_block["start"] :]
                            )
                        else:
                            blocks.append(line)
                            continue

                    else:
                        last_block["text"] += "\n" + line["text"]

                elif last_block["type"] == "text":
                    last_block["text"] += "\n" + line["text"]

            last_line = line

        # Replace blocks text with block children
        for block in blocks:
            text = block.pop("text")
            block["children"] = [text]

        # Merge blocks
        merged_blocks: list[dict] = []
        for block in blocks:
            if not merged_blocks:
                merged_blocks.append(block)
                continue

            last_block = merged_blocks[-1]
            if block["type"] == "list":
                if (
                    last_block["type"] == "list"
                    and block["delimiter"] == last_block["delimiter"]
                ):
                    last_block["children"] += block["children"]
                else:
                    merged_blocks.append(block)

            else:
                merged_blocks.append(block)

        return merged_blocks

    def split_match_into_lines(self, match: str) -> list[dict]:
        lines = [self.parse_match_line(line) for line in match.splitlines()]

        # Strip blank lines separating list items from each other
        clean_lines: list[dict] = []
        for line in reversed(lines):
            if line["type"] != "blank":
                clean_lines.append(line)
            elif clean_lines and clean_lines[-1]["type"] != "line":
                clean_lines.append(line)

        clean_lines.reverse()
        return clean_lines

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
            "text": line_clean[1:] if line_clean.strip() else "",
        }
