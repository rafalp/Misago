from ..outlets import PluginOutlet, append_outlet_action, template_outlet_action


@template_outlet_action
def noop_action(request, context):
    return None


def test_noop_template_action_renders_nothing(
    patch_outlets, render_outlet_template, snapshot
):
    append_outlet_action(PluginOutlet.TEST, noop_action)
    html = render_outlet_template()
    assert snapshot == html


@template_outlet_action
def template_name_action(request, context):
    return "misago/template_outlet_action_test.html"


def test_template_name_action_renders_template_with_standard_context(
    patch_outlets, render_outlet_template, snapshot
):
    append_outlet_action(PluginOutlet.TEST, template_name_action)
    html = render_outlet_template({"message": "Standard context"})
    assert snapshot == html


@template_outlet_action
def template_name_context_action(request, context):
    return "misago/template_outlet_action_test.html", {"message": "Custom context"}


def test_template_name_context_action_renders_template_with_updated_context(
    patch_outlets, render_outlet_template, snapshot
):
    append_outlet_action(PluginOutlet.TEST, template_name_context_action)
    html = render_outlet_template({"message": "Standard context"})
    assert snapshot == html
