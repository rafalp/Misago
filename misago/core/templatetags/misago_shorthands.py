from django import template


register = template.Library()


@register.filter
def iftrue(value, test):
    return value if test else ""


@register.filter
def iffalse(value, test):
    return "" if test else value
