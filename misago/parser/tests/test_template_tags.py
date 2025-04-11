from django.template import Context, Template


def render(template_str, context: dict | None = None):
    base_template = "{%% load misago_rich_text %%} %s"
    context = Context(context or {})
    template = Template(base_template % template_str)
    return template.render(context).strip()


def test_complete_markup_template_tag_passes_args_to_replace_rich_text_tokens(
    mocker, parse_to_html, thread, user
):
    replace_rich_text_tokens_mock = mocker.patch(
        "misago.parser.templatetags.misago_rich_text.replace_rich_text_tokens"
    )

    html = parse_to_html("[quote]Hello world![/quote]")
    posts_data = {"metadata": True}
    context = {
        "my_thread": thread,
        "user": user,
        "html": html,
        "posts_data": posts_data,
    }

    render("{% rich_text html posts_data thread=my_thread %}", context)

    replace_rich_text_tokens_mock.assert_called_once_with(
        html, Context(context), posts_data, thread
    )


def test_complete_markup_template_tag_replaces_intermediate_html(
    parse_to_html, snapshot
):
    html = parse_to_html("[quote]Hello world![/quote]")
    assert snapshot == render("{% rich_text html %}", {"html": html})
