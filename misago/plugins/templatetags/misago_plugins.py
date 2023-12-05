from django import template
from django.utils.safestring import mark_safe

from ..outlets import template_outlets

register = template.Library()


@register.simple_tag(takes_context=True)
def pluginoutlet(context, name: str):
    if name not in template_outlets:
        return None

    content = ""
    for plugin_content in template_outlets[name](context):
        if plugin_content is not None:
            content += plugin_content
    return mark_safe(content)
