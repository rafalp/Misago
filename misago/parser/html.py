from markdown_it import MarkdownIt
from markdown_it.token import Token


def render_tokens_to_html(parser: MarkdownIt, tokens: list[Token]) -> str:
    return parser.renderer.render(tokens, parser.options, {}).strip()
