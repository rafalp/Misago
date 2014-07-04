import bleach
from django import template


register = template.Library()


@register.filter(name='linkify', is_safe=True)
def linkify(string):
    return bleach.linkify(string)
