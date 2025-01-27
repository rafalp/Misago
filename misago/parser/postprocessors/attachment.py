from ..parser import Parser


class AttachmentPostProcessor:
    valid_parents = ["quote", "quote-bbcode", "spoiler"]

    def __call__(self, parser: Parser, ast: list[dict]) -> list[dict]:
        new_ast: list[dict] = []
        for node in ast:
            new_ast += self.process_node(node)
        return new_ast

    def process_node(self, node: dict) -> list[dict]:
        if "children" not in node:
            return [node]

        if node["type"] in self.valid_parents:
            return self.process_valid_parent(node)

        return self.process_invalid_parent(node)

    def process_valid_parent(self, node: dict) -> list[dict]:
        new_children: list[dict] = []
        for child in node["children"]:
            new_children += self.process_node(child)
        node["children"] = new_children
        return [node]

    def process_invalid_parent(self, node: dict) -> list[dict]:
        flat_children: list[dict] = []
        for child in node["children"]:
            flat_children += self.process_node(child)

        new_ast: list[dict] = []
        new_children: list[dict] = []
        for child in flat_children:
            if child["type"] == "attachment":
                if new_children:
                    node_copy = node.copy()
                    node_copy["children"] = new_children
                    new_ast.append(node_copy)
                    new_children = []

                new_ast.append(child)
            else:
                new_children += self.process_node(child)

        if new_children:
            node["children"] = new_children
            new_ast.append(node)

        return new_ast
