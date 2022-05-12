from typing import List

BLOCK_OPEN = "block_open"
BLOCK_CLOSE = "block_close"
BLOCK_NODES = (BLOCK_OPEN, BLOCK_CLOSE)


def restructure_generic_blocks(ast: List[dict]) -> List[dict]:
    """Takes AST with inline generic blocks and returns new AST with proper AST"""
    ast = extract_generic_blocks_from_paragraphs(ast)
    return wrap_generic_blocks(ast)


def extract_generic_blocks_from_paragraphs(ast: List[dict]) -> List[dict]:
    new_ast: List[dict] = []
    for node in ast:
        if node["type"] == "paragraph":
            new_ast.extend(split_paragraph_ast(node))
        else:
            if "children" in node:
                node["children"] = extract_generic_blocks_from_paragraphs(
                    node["children"]
                )
            new_ast.append(node)

    return new_ast


def split_paragraph_ast(node: dict) -> List[dict]:
    """Splits paragraph AST into multiple paragraphs intervined with generic blocks."""
    new_ast: List[dict] = []
    new_children: List[dict] = []

    for child_node in node["children"]:
        if child_node["type"] in BLOCK_NODES:
            if new_children:
                new_ast.append(
                    {
                        "type": "paragraph",
                        "children": new_children,
                    }
                )
                new_children = []
            new_ast.append(child_node)
        else:
            new_children.append(child_node)

    if new_children:
        new_ast.append(
            {
                "type": "paragraph",
                "children": new_children,
            }
        )

    return new_ast


def wrap_generic_blocks(ast: List[dict]) -> List[dict]:
    find_blocks_pairs(ast)

    stack: List[dict] = [{"children": []}]
    for node in remove_invalid_blocks(ast):
        if node["type"] == BLOCK_OPEN:
            node["children"] = []
            stack.append(node)
        elif node["type"] == BLOCK_CLOSE:
            closed_stack = stack.pop(-1)
            new_node = closed_stack["ast"]
            new_node["children"] = closed_stack["children"]
            stack[-1]["children"].append(new_node)
        else:
            if "children" in node and node["type"] not in ("paragraph", "block_text"):
                node["children"] = wrap_generic_blocks(node["children"])
            stack[-1]["children"].append(node)

    return stack[0]["children"]


def find_blocks_pairs(ast: List[dict]):
    stack: List[dict] = []
    counter = 0

    for node in ast:
        if node["type"] == BLOCK_OPEN:
            counter += 1
            node["block_id"] = f'{node["block_type"]}:{counter}'
            stack.append(node)

        if node["type"] == BLOCK_CLOSE:
            if stack:
                while stack:
                    opening_node = stack.pop(-1)
                    if opening_node["block_type"] == node["block_type"]:
                        node["block_id"] = opening_node["block_id"]
                        break

                    opening_node["block_id"] = None
            else:
                node["block_id"] = None

    for node in stack:
        node["block_id"] = None


def remove_invalid_blocks(ast: List[dict]) -> List[dict]:
    new_ast: List[dict] = []
    for node in ast:
        if node["type"] in BLOCK_NODES:
            if node["block_id"] is not None:
                new_ast.append(node)
            else:
                new_ast.append(
                    {
                        "type": "paragraph",
                        "children": [{"type": "text", "text": node["fallback"]}],
                    }
                )
        else:
            new_ast.append(node)

    return new_ast
