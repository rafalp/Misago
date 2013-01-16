import math
import urllib
from coffin.template import Library
from django.conf import settings
from misago.utils import slugify

register = Library()

@register.object(name='widthratio')
def widthratio(min=0, max=100, range=100):
    return int(math.ceil(float(float(min) / float(max) * int(range))))


@register.object(name='query')
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
def slugify_tag(format_string):
    return slugify(format_string)


"""
Markdown filters
"""
@register.filter(name='markdown')
def parse_markdown(value, format=None):
    import markdown
    if not format:
        format = settings.OUTPUT_FORMAT
    return markdown.markdown(value, safe_mode='escape', output_format=format)

@register.filter(name='markdown_short')
def short_markdown(value, length=300):
    from misago.markdown.factory import clear_markdown
    value = clear_markdown(value)
    if len(value) <= length:
        return ' '.join(value.splitlines())
    value = ' '.join(value.splitlines())
    value = value[0:length]
    while value[-1] != ' ':
        value = value[0:-1]
    value = value.strip()
    if value[-3:3] != '...':
        value = '%s...' % value
    return value


"""
Date and time filters
"""
from datetime import datetime, timedelta
from django.utils.dateformat import format, time_format
from django.utils.timezone import is_aware, localtime, utc
from django.utils.translation import pgettext, ungettext, ugettext as _
from misago.utils import slugify, formats

def date(val, arg=""):
    if not arg:
        arg = formats['DATE_FORMAT']
    elif arg in formats:
        arg = formats[arg]
    return format(localtime(val), arg)


def reldate(val, arg=""):
    now = datetime.now(utc if is_aware(val) else None)
    local_now = localtime(now)
    diff = now - val
    local = localtime(val)

    # Today check
    if format(local, 'Y-z') == format(local_now, 'Y-z'):
        return _("Today, %(hour)s") % {'hour': time_format(local, formats['TIME_FORMAT'])}
    # Yesteday check
    yesterday = localtime(now - timedelta(days=1))
    if format(local, 'Y-z') == format(yesterday, 'Y-z'):
        return _("Yesterday, %(hour)s") % {'hour': time_format(local, formats['TIME_FORMAT'])}
    # Tomorrow Check
    tomorrow = localtime(now + timedelta(days=1))
    if format(local, 'Y-z') == format(tomorrow, 'Y-z'):
        return _("Tomorrow, %(hour)s") % {'hour': time_format(local, formats['TIME_FORMAT'])}
    # Day of Week check
    if format(local, 'D') != format(local_now, 'D') and (diff.days > -7 or diff.days < 7):
        return _("%(day)s, %(hour)s") % {'day': format(local, 'l'), 'hour': time_format(local, formats['TIME_FORMAT'])}

    # Fallback to custom      
    return date(val, arg)


def reltimesince(val, arg=""):
    now = datetime.now(utc if is_aware(val) else None)
    diff = now - val
    local = localtime(val)

    # Difference is greater than day for sure
    if diff.days != 0:
        return reldate(val, arg)

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
    return reldate(val, arg)

@register.filter(name='date')
def date_filter(val, arg=""):
    return date(val, arg)


@register.filter(name='reldate')
def reldate_filter(val, arg=""):
    return reldate(val, arg)


@register.filter(name='reltimesince')
def reltimesince_filter(val, arg=""):
    return reltimesince(val, arg)
