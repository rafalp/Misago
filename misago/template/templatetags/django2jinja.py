import urllib
from coffin.template import Library
register = Library()

@register.object(name='widthratio')
def widthratio(min=0, max=100, range=100):
    return int(float(min) / float(max) * int(range))


@register.object(name='query')
def query_string(**kwargs):
    query = urllib.urlencode(kwargs)
    return '?%s' % query if kwargs else ''