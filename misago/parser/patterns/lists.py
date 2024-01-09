import re
from textwrap import dedent

from ..parser import Parser, Pattern

LIST_PATTERN = r"(\n|^) *([-*+]|(1[.)])).+(\n\n* *([-*+]|([0-9]+[.)])).+)*"
LIST_CONTENTS = re.compile(r"(?P<prefix> *)(?P<marker>[-*+]|([0-9]+[.)]))(?P<text>.+)")


class ListMarkdown(Pattern):
    pattern: str = LIST_PATTERN

    def parse(self, parser: Parser, match: str) -> list[dict]:
        items = parse_list_items(parser, match)
        return get_lists_from_items(items)


def parse_list_items(parser: Parser, match: str) -> list[tuple[int, str, list[dict]]]:
    items: list[tuple[int, str, list[dict]]] = []
    for item in LIST_CONTENTS.finditer(dedent(match)):
        level = len(item.group("prefix") or "")
        if level % 2 != 0:
            level -= 1
        if level:
            level = int(level / 2)  # TODO: normalize levels across items somehow

        marker = item.group("marker")
        if marker not in "-*+":
            marker = "n"

        text = item.group("text").strip()
        items.append((level, marker, parser.parse_inline(text)))

    return items


def get_lists_from_items(
    items: list[tuple[int, str, list[dict]]],
) -> list[dict]:
    lists_asts: list[dict] = []
    lists_stack: list[dict] = []

    level: int = -1
    marker: str | None = None

    for item_level, item_marker, children in items:
        if item_level != level or item_marker != marker:
            # Fixme: this always makes new list when item_level < level
            list_ast = {
                "type": "list",
                "ordered": item_marker == "n",
                "items": [],
            }

            # Remove N levels from stack
            if item_level < level:
                for _ in range(level - item_level):
                    print("POP")
                    lists_stack.pop(-1)

            elif item_level == level:
                lists_stack.pop(-1)

            if not lists_stack:
                lists_asts.append(list_ast)

            if lists_stack:
                lists_stack[-1]["items"][-1]["lists"].append(list_ast)

            lists_stack.append(list_ast)
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
