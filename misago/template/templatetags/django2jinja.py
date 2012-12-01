from datetime import date, datetime, timedelta
import math
import urllib
from coffin.template import Library
from django.utils.timezone import is_aware, utc
from django.utils.translation import pgettext, ungettext, ugettext as _

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


@register.filter(name='low')
def low(value):
    if not value:
        return u''
    try:
        rest = value[1:]
    except IndexError:
        rest = ''
    return '%s%s' % (unicode(value[0]).lower(), rest)


@register.filter(name='date')
def date(date, arg=""):
    from django.utils.dateformat import format, time_format
    from misago.utils import formats
    
    if not arg:
        arg = formats['DATE_FORMAT']
    elif arg in formats:
        arg = formats[arg]
        
    return format(date, arg)


@register.filter(name='reldate')
def reldate(date, arg=""):
    from django.utils.dateformat import format, time_format
    from misago.utils import formats
    
    now = datetime.now(utc if is_aware(date) else None)
    diff = now - date
    print diff
    
    # Common situations
    if diff.days == 0:
        return _("Today, %(hour)s") % {'hour': time_format(date, formats['TIME_FORMAT'])}
    if diff.days == 1:
        return _("Yesterday, %(hour)s") % {'hour': time_format(date, formats['TIME_FORMAT'])}
    if diff.days == -1:
        return _("Tomorrow, %(hour)s") % {'hour': time_format(date, formats['TIME_FORMAT'])}
    if diff.days > -7 or diff.days < 7:
        return _("%(day)s, %(hour)s") % {'day': format(date, 'l'), 'hour': time_format(date, formats['TIME_FORMAT'])}
    
    # Custom
    if not arg:
        arg = formats['DATE_FORMAT']
    elif arg in formats:
        arg = formats[arg]
        
    return format(date, arg)