from django.contrib.auth import get_user_model
from django.http import HttpRequest

from .ast import filter_ast
from .enums import ContentType
from .factory import create_markdown
from .metadata import get_ast_metadata

User = get_user_model()


def parse_user_signature(
    user: User,
    markup: str,
    *,
    request: HttpRequest | None = None,
    site_urls: list[str] | None = None,
) -> tuple[list, dict]:
    markdown = create_markdown(
        user=User,
        request=request,
        content_type=ContentType.SIGNATURE,
    )

    ast = markdown(markup)
    ast = filter_ast(ast, content_type=ContentType.SIGNATURE)
    return ast, get_ast_metadata(ast)
