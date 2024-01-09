import re
from textwrap import dedent

from ..parser import Parser, Pattern

LIST_PATTERN = r"(\n|^) *([-*+]|(1[.)])).+(\n\n* *([-*+]|([0-9]+[.)])).+)*"
LIST_CONTENTS = re.compile(r"(?P<prefix> )*(?P<marker>[-*+]|([0-9]+[.)]))(?P<text>.+)")


class ListMarkdown(Pattern):
    pattern: str = r"(\n|^)[-*+].*(\n\n*\s*?[-*+].*)*"

    def parse(self, parser: Parser, match: str) -> list[dict]:
        items = parse_list_items(parser, match)

        items_ast: list[dict] = []
        for item in items:
            items_ast.append(
                {
                    "type": "list-item",
                    "children": item[1],
                    "lists": [],
                }
            )

        return {
            "type": "list",
            "ordered": False,
            "items": items_ast,
        }


def parse_list_items(parser: Parser, match: str) -> list[tuple[int, str, list[dict]]]:
    items: list[tuple[int, str, list[dict]]] = []
    for item in LIST_CONTENTS.finditer(dedent(match)):
        previous_depth = items[-1][0] if items else 0
        depth = len(item.group("prefix") or "")
        if depth % 2 != 0:
            depth -= 1
        if depth > previous_depth:
            depth = previous_depth + 1

        text = item.group("text").strip()
        items.append((depth, item.group("marker"), parser.parse_inline(text)))

    return items
