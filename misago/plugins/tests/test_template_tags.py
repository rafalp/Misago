from contextlib import contextmanager

from django.template import Context, Template
from django.utils.safestring import mark_safe

from ..outlets import (
    PluginOutletName,
    PluginOutletHook,
    append_outlet_action,
    prepend_outlet_action,
    template_outlets,
)


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


def strong_action(context):
    body = context.get("value") or "none"
    return mark_safe(f"<strong>{body}</strong>")


def em_action(context):
    body = context.get("value") or "none"
    return mark_safe(f"<em>{body}</em>")


def render_outlet_template(context: dict | None = None):
    template = Template(
        """
        {% load misago_plugins %}
        <div>{% pluginoutlet TEST %}</div>
        """
    )

    return template.render(Context(context or {})).strip()


def test_empty_outlet_renders_nothing(snapshot):
    with patch_outlets():
        html = render_outlet_template()

    assert snapshot == html


def test_outlet_renders_appended_plugin(snapshot):
    with patch_outlets():
        append_outlet_action(PluginOutletName.TEST, strong_action)
        html = render_outlet_template()

    assert snapshot == html


def test_outlet_renders_prepended_plugin(snapshot):
    with patch_outlets():
        prepend_outlet_action(PluginOutletName.TEST, strong_action)
        html = render_outlet_template()

    assert snapshot == html


def test_outlet_renders_multiple_plugins(snapshot):
    with patch_outlets():
        append_outlet_action(PluginOutletName.TEST, strong_action)
        prepend_outlet_action(PluginOutletName.TEST, em_action)
        prepend_outlet_action(PluginOutletName.TEST, strong_action)
        html = render_outlet_template()

    assert snapshot == html


def test_outlet_renders_plugins_with_context(snapshot):
    with patch_outlets():
        append_outlet_action(PluginOutletName.TEST, strong_action)
        prepend_outlet_action(PluginOutletName.TEST, em_action)
        prepend_outlet_action(PluginOutletName.TEST, strong_action)
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


def test_hasplugins_tag_renders_nothing_if_no_plugins_exist(snapshot):
    with patch_outlets():
        html = render_hasplugins_template()

    assert snapshot == html


def test_hasplugins_tag_renders_value_if_plugins_exist(snapshot):
    with patch_outlets():
        append_outlet_action(PluginOutletName.TEST, strong_action)
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


def test_hasplugins_else_tag_renders_else_if_no_plugins_exist(snapshot):
    with patch_outlets():
        html = render_haspluginselse_template()

    assert snapshot == html


def test_hasplugins_else_tag_renders_value_if_plugins_exist(snapshot):
    with patch_outlets():
        append_outlet_action(PluginOutletName.TEST, strong_action)
        html = render_haspluginselse_template()

    assert snapshot == html
