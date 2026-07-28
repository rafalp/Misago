from django.template import Context, Template


def render_to_str(template: str, context: dict | None = None) -> str:
    template_obj = Template(template)
    return template_obj.render(Context(context or {})).strip()


def test_strformat_formats_str():
    result = render_to_str(
        "{% load misago_formats %}{% strformat str val=value %}",
        {"str": "<b>%(val)s</b>", "value": "<hr>"},
    )

    assert result == "&lt;b&gt;&lt;hr&gt;&lt;/b&gt;"


def test_safestrformat_formats_str():
    result = render_to_str(
        "{% load misago_formats %}{% safestrformat str val=value %}",
        {"str": "<b>%(val)s</b>", "value": "<hr>"},
    )

    assert result == "<b><hr></b>"
