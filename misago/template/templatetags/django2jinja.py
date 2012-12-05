from datetime import date, datetime, timedelta
import math
import urllib
from coffin.template import Library
from django.conf import settings
from django.utils.dateformat import format, time_format
from django.utils.timezone import is_aware, utc
from django.utils.translation import pgettext, ungettext, ugettext as _
from misago.utils import slugify, formats

register = Library()

@register.object(name='widthratio')
def widthratio(min=0, max=100, range=100):
    return int(math.ceil(float(float(min) / float(max) * int(range))))


@register.object(name='query')
def query_string(**kwargs):
    query = urllib.urlencode(kwargs)
    return '?%s' % (query if kwargs else '')


@register.filter(name='markdown')
def parse_markdown(value, format=None):
    import markdown
    if not format:
        format = settings.OUTPUT_FORMAT
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
    if not arg:
        arg = formats['DATE_FORMAT']
    elif arg in formats:
        arg = formats[arg]
        
    return format(date, arg)


@register.filter(name='reldate')
def reldate(date, arg=""):
    now = datetime.now(utc if is_aware(date) else None)
    diff = now - date
    
    # Common situations
    if diff.days == 0:
        return _("Today, %(hour)s") % {'hour': time_format(date, formats['TIME_FORMAT'])}
    if diff.days == 1:
        return _("Yesterday, %(hour)s") % {'hour': time_format(date, formats['TIME_FORMAT'])}
    if diff.days == -1:
        return _("Tomorrow, %(hour)s") % {'hour': time_format(date, formats['TIME_FORMAT'])}
    if diff.days > -7 or diff.days < 7:
        return _("%(day)s, %(hour)s") % {'day': format(date, 'l'), 'hour': time_format(date, formats['TIME_FORMAT'])}
    
    # Fallback to custom      
    return date[1](date, arg)


@register.filter(name='reltimesince')
def reltimesince(date, arg=""):
    now = datetime.now(utc if is_aware(date) else None)
    diff = now - date
    
    # Display specific time
    if diff.seconds >= 0:
        if diff.seconds <= 60:
            return _("Minute ago")
        if diff.seconds < 3600:
            minutes = int(math.floor(diff.seconds / 60.0))
            return ungettext(
                    "Minute ago",
                    "%(minutes)s minutes ago",
                minutes) % {'minutes': minutes}
        if diff.seconds < 10800:
            hours = int(math.floor(diff.seconds / 3600.0))
            minutes = (diff.seconds - (hours * 3600)) / 60
            if minutes > 0:
                return ungettext(
                    "Hour and %(minutes)s ago",
                    "%(hours)s hours and %(minutes)s ago",
                hours) % {'hours': hours, 'minutes': ungettext(
                        "%(minutes)s minute",
                        "%(minutes)s minutes",
                    minutes) % {'minutes': minutes}}
                return _("%(hours)s hours and %(minutes)s minutes ago") % {'hours': hours, 'minutes': minutes}
            return ungettext(
                    "Hour ago",
                    "%(hours)s hours ago",
                hours) % {'hours': hours}
        
    # Fallback to reldate
    return reldate[1](date, arg)


@register.filter(name="slugify")
def slugify_tag(format_string):
    return slugify(format_string)