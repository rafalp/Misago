import pytest
from django.template import Context, Template

from ..outlets import PluginOutletHook, template_outlets


@pytest.fixture
def patch_outlets():
    try:
        org_outlets = template_outlets.copy()
        for key in template_outlets:
            template_outlets[key] = PluginOutletHook()
        yield template_outlets
    finally:
        for key, hook in org_outlets.items():
            template_outlets[key] = hook


@pytest.fixture
def render_outlet_template():
    def render_outlet_template_function(context: dict | None = None):
        template = Template(
            """
            {% load misago_plugins %}
            <div>{% pluginoutlet TEST %}</div>
            """
        )

        return template.render(Context(context or {})).strip()

    return render_outlet_template_function
