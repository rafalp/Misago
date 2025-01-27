from ..html import render_ast_to_html
from ..metadata import create_ast_metadata
from ..richtext import replace_rich_text_tokens


def test_replace_rich_text_tokens_replaces_default_spoiler_summary(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("[spoiler]Hello world![/spoiler]")
    metadata = create_ast_metadata(parser_context, ast)
    html = render_ast_to_html(parser_context, ast, metadata)
    assert snapshot == replace_rich_text_tokens(html)
