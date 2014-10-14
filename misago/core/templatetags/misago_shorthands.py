from django import template


register = template.Library()


@register.filter
def iftrue(test, value):
    return value if test else ""


@register.filter
def iffalse(test, value):
    return "" if test else value
