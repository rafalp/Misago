from django import template

register = template.Library()


@register.filter
def isdescriptionshort(string):
    string_lowered = string.lower()
    return string_lowered.count("<p") == 1 and not string_lowered.count("<br")
