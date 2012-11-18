import math
import urllib
from coffin.template import Library
register = Library()

@register.object(name='widthratio')
def widthratio(min=0, max=100, range=100):
    return int(math.ceil(float(float(min) / float(max) * int(range))))


@register.object(name='query')
def query_string(**kwargs):
    query = urllib.urlencode(kwargs)
    return '?%s' % (query if kwargs else '')


@register.filter(name='markdown')
def parse_markdown(value, format="html5"):
    import markdown
    return markdown.markdown(value, safe_mode='escape', output_format=format)