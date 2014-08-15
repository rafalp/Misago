from django import template


register = template.Library()


@register.filter
def striplinebreaks(string):
    if string:
        return ' '.join([s.strip() for s in string.splitlines() if s.strip()])
    else:
        return ''
