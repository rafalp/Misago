from mistune import Markdown

from ..types import RichText, GraphQLContext
from .markdown import ast_markdown, html_markdown


async def parse_markup(context: GraphQLContext, markup: str) -> RichText:
    return ast_markdown(markup)


def create_markdown(context: GraphQLContext) -> Markdown:
    pass


def markup_as_html(markup: str) -> str:
    return html_markdown(markup)
