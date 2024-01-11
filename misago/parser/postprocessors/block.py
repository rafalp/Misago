from ..parser import Parser


class BlockPostProcessor:
    opening_type: str
    closing_type: str

    def __call__(self, parser: Parser, ast: list[dict]) -> list[dict]:
        new_ast: list[dict] = []

        stack: list[tuple[dict, list[dict]]] = []
        for block_ast in ast:
            if block_ast["type"] == self.opening_type:
                stack.append((block_ast, []))
            elif stack:
                if block_ast["type"] == self.closing_type:
                    opening_block, children = stack.pop(-1)
                    wrapped_block = self.wrap_block(
                        parser, opening_block, block_ast, children
                    )
                    if wrapped_block:
                        if stack:
                            stack[-1][1].append(wrapped_block)
                        else:
                            new_ast.append(wrapped_block)
                else:
                    stack[-1][1].append(self.process_other_block(parser, block_ast))
            else:
                new_ast.append(self.process_other_block(parser, block_ast))

        for opening_block, children in stack:
            new_ast.append(opening_block)
            new_ast += self(parser, children)

        return new_ast

    def wrap_block(
        self,
        parser: Parser,
        opening_block: dict,
        closing_block: dict,
        children: list[dict],
    ) -> dict | None:
        if not children:
            return None

        new_children: list[dict]
        for block_ast in children:
            new_children.append(self.process_other_block(parser, block_ast))
        return new_children

    def process_other_block(self, parser: Parser, block_ast: dict) -> dict:
        if block_ast["type"] != "paragraph" and block_ast.get("children"):
            block_ast["children"] = self(parser, block_ast["children"])
        return block_ast
