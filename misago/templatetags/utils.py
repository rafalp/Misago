from coffin.template import Library
from misago.utils.strings import short_string

register = Library()


@register.object(name='intersect')
def intersect(list_a, list_b):
    for i in list_a:
        if i in list_b:
            return True
    return False


@register.filter(name='short_string')
def make_short(string, length=16):
    return short_string(string, length)