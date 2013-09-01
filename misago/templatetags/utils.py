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


@register.global_function(name='color')
def color_wheel(index):
    while index > 15:
        index -= 15
    colors = (
              (49, 130, 189),
              (49, 163, 84),
              (230, 85, 13),
              (117, 107, 177),
              (222, 45, 38),
              (158, 202, 225),
              (161, 217, 155),
              (253, 174, 107),
              (188, 189, 220),
              (252, 146, 114),
              (222, 235, 247),
              (229, 245, 224),
              (254, 230, 206),
              (239, 237, 245),
              (254, 224, 210),
             )
    return colors[index]


@register.global_function(name='colorhex')
def color_hex(index):
    color = color_wheel(index)
    r = unicode(hex(color[0])[2:])
    if len(r) == 0:
        r = '0%s' % r
    g = unicode(hex(color[1])[2:])
    if len(g) == 0:
        g = '0%s' % g
    b = unicode(hex(color[2])[2:])
    if len(b) == 0:
        b = '0%s' % b
    return r+g+b