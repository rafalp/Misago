from ..parser import Parser


class MergeListsASTPostProcessor:
    def __call__(self, parser: Parser, ast: list[dict]) -> list[dict]:
        new_ast: list[dict] = []
        for node in ast:
            if "children" in node:
                node["children"] = self(parser, node["children"])

            if (
                node["type"] == "list"
                and new_ast
                and new_ast[-1]["type"] == "list"
                and node["delimiter"] == new_ast[-1]["delimiter"]
            ):
                new_ast[-1]["tight"] = False
                new_ast[-1]["children"] += node["children"]
                continue

            new_ast.append(node)

        return new_ast
