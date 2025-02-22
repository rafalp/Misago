from django.conf import settings

from ..parser import Parser


class CleanASTPostProcessor:
    valid_attachment_parents = [
        "quote",
        "quote-bbcode",
        "spoiler",
        "list-item",
        "table-cell",
    ]
    valid_empty_nodes = [
        "table",
        "table-header",
        "table-cell",
        "image-bbcode",
        "url-bbcode",
    ]

    def __call__(self, parser: Parser, ast: list[dict]) -> list[dict]:
        if not settings.MISAGO_PARSER_CLEAN_AST:
            return ast

        new_ast: list[dict] = []
        for node in ast:
            new_ast += self.process_node(node)
        return new_ast

    def process_node(self, node: dict) -> list[dict]:
        if "children" not in node:
            return [node]

        if node["type"] in self.valid_attachment_parents:
            return self.process_valid_parent(node)

        return self.process_invalid_parent(node)

    def process_valid_parent(self, node: dict) -> list[dict]:
        new_children: list[dict] = []
        for child in node["children"]:
            new_children += self.process_node(child)
        node["children"] = new_children
        return [node]

    def process_invalid_parent(self, node: dict) -> list[dict]:
        valid_empty_node = node["type"] in self.valid_empty_nodes

        flat_children: list[dict] = []
        for child in node["children"]:
            flat_children += self.process_node(child)

        new_ast: list[dict] = []
        new_children: list[dict] = []
        for child in flat_children:
            if child["type"] == "attachment":
                if new_children or valid_empty_node:
                    node_copy = node.copy()
                    node_copy["children"] = new_children
                    new_ast.append(node_copy)
                    new_children = []

                if not new_ast or new_ast[-1]["type"] != "attachment-group":
                    new_ast.append({"type": "attachment-group", "children": []})

                new_ast[-1]["children"].append(child)
            else:
                new_children += self.process_node(child)

        if new_children:
            node["children"] = new_children
            new_ast.append(node)

        # Re-insert node in new AST if it's valid empty node
        # and above logic omitted it
        if valid_empty_node and node["type"] not in [n["type"] for n in new_ast]:
            node_copy = node.copy()
            node_copy["children"] = []
            new_ast.insert(0, node_copy)

        return new_ast
