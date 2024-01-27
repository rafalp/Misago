from django.template import Context, Template

from ..html import complete_markup_html, render_ast_to_html
from ..metadata import create_ast_metadata


def render(template_str, context: dict | None = None):
    base_template = "{%% load misago_markup %%} %s"
    context = Context(context or {})
    template = Template(base_template % template_str)
    return template.render(context).strip()


def test_complete_markup_template_tag_replaces_default_spoiler_summary(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("[spoiler]Hello world![/spoiler]")
    metadata = create_ast_metadata(parser_context, ast)
    html = render_ast_to_html(parser_context, ast, metadata)
    assert snapshot == render("{% completemarkup html %}", {"html": html})
