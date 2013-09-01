from django_jinja.library import Library
from haystack.utils import Highlighter
from misago.utils.strings import short_string

register = Library()


@register.global_function(name='intersect')
def intersect(list_a, list_b):
    for i in list_a:
        if i in list_b:
            return True
    return False


@register.filter(name='short_string')
def make_short(string, length=16):
    return short_string(string, length)


@register.filter(name='highlight')
def highlight_result(text, query, length=500):
    hl = Highlighter(query, html_tag='strong', max_length=length)
    hl = hl.highlight(text)
    return hl