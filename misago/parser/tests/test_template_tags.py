from django.template import Context, Template


def render(template_str, context: dict | None = None):
    base_template = "{%% load misago_rich_text %%} %s"
    context = Context(context or {})
    template = Template(base_template % template_str)
    return template.render(context).strip()


def test_complete_markup_template_tag_replaces_default_spoiler_summary(
    parse_to_html, snapshot
):
    html = parse_to_html("[spoiler]Hello world![/spoiler]")
    assert snapshot == render("{% rich_text html %}", {"html": html})
