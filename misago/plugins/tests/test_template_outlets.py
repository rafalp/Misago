from contextlib import contextmanager

from django.template import Context, Template

from ..outlets import (
    PluginOutletName,
    PluginOutletHook,
    append_template_plugin,
    prepend_template_plugin,
    template_outlets,
)


def strong_action(context):
    body = context.get("value") or "none"
    return f"<strong>{body}</strong>"


def em_action(context):
    body = context.get("value") or "none"
    return f"<em>{body}</em>"


def render_template(context: dict | None = None):
    template = Template(
        """
        {% load misago_plugins %}
        <div>{% pluginoutlet "TEST" %}</div>
        """
    )

    return template.render(Context(context or {})).strip()


@contextmanager
def patch_outlets():
    try:
        org_outlets = template_outlets.copy()
        for key in template_outlets:
            template_outlets[key] = PluginOutletHook()
        yield template_outlets
    finally:
        for key, hook in org_outlets.items():
            template_outlets[key] = hook


def test_empty_outlet_renders_nothing(snapshot):
    with patch_outlets():
        html = render_template()

    assert snapshot == html


def test_outlet_renders_appended_plugin(snapshot):
    with patch_outlets():
        append_template_plugin(PluginOutletName.TEST, strong_action)
        html = render_template()

    assert snapshot == html


def test_outlet_renders_prepended_plugin(snapshot):
    with patch_outlets():
        prepend_template_plugin(PluginOutletName.TEST, strong_action)
        html = render_template()

    assert snapshot == html


def test_outlet_renders_multiple_plugins(snapshot):
    with patch_outlets():
        append_template_plugin(PluginOutletName.TEST, strong_action)
        prepend_template_plugin(PluginOutletName.TEST, em_action)
        prepend_template_plugin(PluginOutletName.TEST, strong_action)
        html = render_template()

    assert snapshot == html


def test_outlet_renders_plugins_with_context(snapshot):
    with patch_outlets():
        append_template_plugin(PluginOutletName.TEST, strong_action)
        prepend_template_plugin(PluginOutletName.TEST, em_action)
        prepend_template_plugin(PluginOutletName.TEST, strong_action)
        html = render_template({"value": "context"})

    assert snapshot == html
