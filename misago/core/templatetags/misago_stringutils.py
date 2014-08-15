from django import template


register = template.Library()


@register.filter
def striplinebreaks(string):
    return ' '.join([s.strip() for s in string.splitlines() if s.strip()])
