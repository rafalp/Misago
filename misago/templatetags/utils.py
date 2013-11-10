from django_jinja.library import Library
from haystack.utils import Highlighter
from misago.utils import colors
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


@register.filter(name='filesize')
def format_filesize(size):
    try:
        for u in ('B','KB','MB','GB','TB'):
            if size < 1024.0:
                return "%3.1f %s" % (size, u)
            size /= 1024.0
    except ValueError:
        return '0 B'


@register.filter(name='highlight')
def highlight_result(text, query, length=500):
    hl = Highlighter(query, html_tag='strong', max_length=length)
    hl = hl.highlight(text)
    return hl


@register.global_function(name='color_spin')
def spin_color_filter(color, spin):
    return colors.spin(color, spin)


@register.global_function(name='color_desaturate')
def desaturate_color_filter(color, steps, step, minimum=0.0):
    return colors.desaturate(color, steps, step, minimum)


@register.global_function(name='color_lighten')
def lighten_color_filter(color, steps, step, maximum=100.0):
    return colors.lighten(color, steps, step, maximum)


@register.global_function(name='color_darken')
def darken_color_filter(color, steps, step, minimum=0.0):
    return colors.darken(color, steps, step, minimum)