from ..parser import Parser


class RemoveRepeatsPostProcessor:
    checked_types: list[str]

    def __call__(self, parser: Parser, ast: list[dict]) -> list[dict]:
        new_ast: list[dict] = []
        for node in ast:
            if (
                node["type"] in self.checked_types
                and new_ast
                and new_ast[-1]["type"] in self.checked_types
            ):
                continue

            if "children" in node:
                node["children"] = self(parser, node["children"])

            new_ast.append(node)

        return new_ast
