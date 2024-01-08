from copy import deepcopy

from django.http import HttpRequest

from .hooks import filter_ast_hook


def filter_ast(
    ast: list, content_type: str | None = None, request: HttpRequest | None = None
) -> list:
    filtered_ast = deepcopy(ast)
    filtered_ast = strip_blank_lines_ast(filtered_ast)
    return filter_ast_hook(_filter_ast_action, ast, content_type, request)


def _filter_ast_action(
    ast: list, content_type: str | None = None, request: HttpRequest | None = None
) -> list:
    return ast


def strip_blank_lines_ast(ast: list) -> list:
    clean_ast = []
    for block_ast in ast:
        if block_ast["type"] == "blank_line":
            continue
        else:
            if "children" in block_ast and block_ast["children"]:
                block_ast["children"] = strip_blank_lines_ast(block_ast["children"])
            clean_ast.append(block_ast)
    return clean_ast
