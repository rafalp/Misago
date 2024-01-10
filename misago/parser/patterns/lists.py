import re
from textwrap import dedent

from ..parser import Parser, Pattern

LIST_PATTERN = r"(\n|^) *([-*+]|(1[.)])).+(\n\n* *([-*+]|([0-9]+[.)])).+)*"
LIST_CONTENTS = re.compile(r"(?P<prefix> *)(?P<marker>[-*+]|([0-9]+[.)]))(?P<text>.+)")

ListItem = tuple[int, str, list[dict]]


class ListMarkdown(Pattern):
    pattern: str = LIST_PATTERN

    def parse(self, parser: Parser, match: str) -> list[dict]:
        items = parse_list_items(parser, match)
        return get_lists_from_items(items)


def parse_list_items(parser: Parser, match: str) -> list[ListItem]:
    items: list[ListItem] = []
    prev_level: int | None = None
    for item in LIST_CONTENTS.finditer(dedent(match).strip()):
        level = len(item.group("prefix") or "")
        if level % 2 != 0:
            level -= 1
        if level:
            level = int(level / 2)

        clean_level = level
        if prev_level is not None:
            if level == prev_level:
                clean_level = items[-1][0]
            elif level > prev_level or level > items[-1][0] + 1:
                clean_level = items[-1][0] + 1

        prev_level = level

        marker = item.group("marker")
        if marker not in "-*+":
            marker = "n"

        text = item.group("text").strip()
        items.append((clean_level, marker, parser.parse_inline(text)))

    return items


def get_lists_from_items(
    items: list[ListItem],
) -> list[dict]:
    lists_asts: list[dict] = []
    lists_stack: list[dict] = []

    level: int = -1
    marker: str | None = None

    for item_level, item_marker, children in items:
        if item_level > level or item_marker != marker:
            list_ast = {
                "type": "list",
                "ordered": item_marker == "n",
                "items": [],
            }

            if item_level == level:
                lists_stack.pop(-1)

            if not lists_stack:
                lists_asts.append(list_ast)

            if lists_stack:
                lists_stack[-1]["items"][-1]["lists"].append(list_ast)

            lists_stack.append(list_ast)

        if item_level < level:
            for _ in range(level - item_level):
                lists_stack.pop(-1)

        if item_level != level or item_marker != marker:
            level = item_level
            marker = item_marker

        lists_stack[-1]["items"].append(
            {
                "type": "list-item",
                "children": children,
                "lists": [],
            }
        )

    return lists_asts
