from django import template
from django.template.loader import get_template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def includecomponents(context, data):
    if not data:
        return ""

    html = []
    for child_component in data:
        component_context = context.flatten()
        component_context.update(child_component)
        template = get_template(child_component["template_name"])
        html.append(template.render(component_context))

    return mark_safe("\n".join(html))


@register.simple_tag(takes_context=True)
def includecomponent(context, data):
    component_context = context.flatten()
    component_context.update(data)
    template = get_template(data["template_name"])
    return mark_safe(template.render(component_context))
