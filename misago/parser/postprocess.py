from copy import deepcopy

from django.http import HttpRequest

from .hooks import filter_ast_hook


def post_process_ast(
    ast: list, content_type: str | None = None, request: HttpRequest | None = None
) -> list:
    processed_ast = deepcopy(ast)
    return filter_ast_hook(
        _post_process_ast_action, processed_ast, content_type, request
    )


def _post_process_ast_action(
    ast: list, content_type: str | None = None, request: HttpRequest | None = None
) -> list:
    return ast
