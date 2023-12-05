from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def pluginoutlet(context, name: str):
    content = []
    return content
