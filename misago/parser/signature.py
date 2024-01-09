from django.contrib.auth import get_user_model
from django.http import HttpRequest

from .enums import ContentType
from .factory import create_parser
from .metadata import get_ast_metadata
from .postprocess import post_process_ast

User = get_user_model()


def parse_user_signature(
    user: User,
    markup: str,
    *,
    request: HttpRequest | None = None,
    site_urls: list[str] | None = None,
) -> tuple[list, dict]:
    parser = create_parser(
        user=User,
        request=request,
        content_type=ContentType.SIGNATURE,
    )

    ast = parser(markup)
    ast = post_process_ast(ast, content_type=ContentType.SIGNATURE)
    return ast, get_ast_metadata(ast)
