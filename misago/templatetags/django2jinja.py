import math
import urllib
from django_jinja.library import Library
from misago.utils.strings import slugify

register = Library()


@register.global_function(name='widthratio')
def widthratio(min=0, max=100, range=100):
    return int(math.ceil(float(float(min) / float(max) * int(range))))


@register.global_function(name='query')
def query_string(**kwargs):
    query = urllib.urlencode(kwargs)
    return '?%s' % (query if kwargs else '')


@register.filter(name='low')
def low(value):
    if not value:
        return u''
    try:
        rest = value[1:]
    except IndexError:
        rest = ''
    return '%s%s' % (unicode(value[0]).lower(), rest)


@register.filter(name="slugify")
def slugify_function(format_string):
    return slugify(format_string)
