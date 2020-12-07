from .markdown import ast_markdown, html_markdown
from ..types import RichText


def parse_markup(markup: str) -> RichText:
    return ast_markdown(markup)


def markup_as_html(markup: str) -> str:
    return html_markdown(markup)
