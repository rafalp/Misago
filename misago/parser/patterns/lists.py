import re
from textwrap import dedent

from ..parser import Parser, Pattern

LIST_PATTERN = r"(\n|^) *([-*+]|(1[.)])).*(\n\n* *([-*+]|([0-9]+[.)])).*)*"
LIST_CONTENTS = re.compile(r"(?P<prefix> *)(?P<marker>[-*+i]|([0-9]+[.)]))(?P<text>.*)")

ListItem = tuple[int, str, list[dict]]


class ListMarkdown(Pattern):
    pattern_type: str = "list"
    pattern: str = LIST_PATTERN

    def parse(self, parser: Parser, match: str, parents: list[str]) -> list[dict]:
        items = self.parse_list_items(
            parser, match, parents + [self.pattern_type, "list-item"]
        )
        return self.get_lists_from_items(items)

    def parse_list_items(
        self, parser: Parser, match: str, parents: list[str]
    ) -> list[ListItem]:
        items: list[ListItem] = []
        prev_level: int | None = None
        for item in LIST_CONTENTS.finditer(dedent(match).strip()):
            raw_level = len(item.group("prefix") or "")

            if not items:
                clean_level = 0
                prev_level = raw_level
            else:
                level_diff = raw_level - prev_level
                if level_diff >= 2:
                    clean_level = items[-1][1] + 1
                elif level_diff >= 0:
                    clean_level = items[-1][1]
                else:
                    clean_level = 0
                    for prev_item in items:
                        if raw_level - prev_item[0] >= 2:
                            clean_level += 1

                prev_level = raw_level

            marker = item.group("marker")
            if marker not in "-*+":
                marker = "n"

            text = item.group("text").strip()
            items.append(
                (
                    raw_level,
                    clean_level,
                    marker,
                    parser.parse_inline(text, parents, reverse_reservations=True),
                )
            )

        return items

    def get_lists_from_items(self, items: list[ListItem]) -> list[dict]:
        lists_asts: list[dict] = []
        lists_stack: list[dict] = []

        level: int = -1
        marker: str | None = None

        for _, item_level, item_marker, children in items:
            if item_level > level or item_marker != marker:
                list_ast = {
                    "type": ListMarkdown.pattern_type,
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
