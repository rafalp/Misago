from django.template import Context, Template
from django.utils.safestring import mark_safe

from ..outlets import PluginOutlet, append_outlet_action, prepend_outlet_action


def strong_action(request, context):
    body = context.get("value") or "none"
    return mark_safe(f"<strong>{body}</strong>")


def em_action(request, context):
    body = context.get("value") or "none"
    return mark_safe(f"<em>{body}</em>")


def test_empty_outlet_renders_nothing(patch_outlets, render_outlet_template, snapshot):
    html = render_outlet_template()
    assert snapshot == html


def test_outlet_renders_appended_plugin(
    patch_outlets, render_outlet_template, snapshot
):
    append_outlet_action(PluginOutlet.TEST, strong_action)
    html = render_outlet_template()

    assert snapshot == html


def test_outlet_renders_prepended_plugin(
    patch_outlets, render_outlet_template, snapshot
):
    prepend_outlet_action(PluginOutlet.TEST, strong_action)
    html = render_outlet_template()

    assert snapshot == html


def test_outlet_renders_multiple_plugins(
    patch_outlets, render_outlet_template, snapshot
):
    append_outlet_action(PluginOutlet.TEST, strong_action)
    prepend_outlet_action(PluginOutlet.TEST, em_action)
    prepend_outlet_action(PluginOutlet.TEST, strong_action)
    html = render_outlet_template()

    assert snapshot == html


def test_outlet_renders_plugins_with_context(
    patch_outlets, render_outlet_template, snapshot
):
    append_outlet_action(PluginOutlet.TEST, strong_action)
    prepend_outlet_action(PluginOutlet.TEST, em_action)
    prepend_outlet_action(PluginOutlet.TEST, strong_action)
    html = render_outlet_template({"value": "context"})

    assert snapshot == html


def render_hasplugins_template(context: dict | None = None):
    template = Template(
        """
        {% load misago_plugins %}
        <div>{% hasplugins TEST %}plugins{% endhasplugins %}</div>
        """
    )

    return template.render(Context(context or {})).strip()


def test_hasplugins_tag_renders_nothing_if_no_plugins_exist(patch_outlets, snapshot):
    html = render_hasplugins_template()

    assert snapshot == html


def test_hasplugins_tag_renders_value_if_plugins_exist(patch_outlets, snapshot):
    append_outlet_action(PluginOutlet.TEST, strong_action)
    html = render_hasplugins_template()

    assert snapshot == html


def render_haspluginselse_template(context: dict | None = None):
    template = Template(
        """
        {% load misago_plugins %}
        <div>{% hasplugins TEST %}plugins{% else %}noplugins{% endhasplugins %}</div>
        """
    )

    return template.render(Context(context or {})).strip()


def test_hasplugins_else_tag_renders_else_if_no_plugins_exist(patch_outlets, snapshot):
    html = render_haspluginselse_template()

    assert snapshot == html


def test_hasplugins_else_tag_renders_value_if_plugins_exist(patch_outlets, snapshot):
    append_outlet_action(PluginOutlet.TEST, strong_action)
    html = render_haspluginselse_template()

    assert snapshot == html
