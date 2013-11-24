import math
from datetime import datetime, timedelta
from django.utils.dateformat import format, time_format
from django.utils.formats import get_format
from django.utils.timezone import is_aware, localtime, utc
from django.utils.translation import pgettext, ungettext, ugettext as _
from misago.utils.strings import slugify

# Build date formats
formats = {
    'DATE_FORMAT': '',
    'DATETIME_FORMAT': '',
    'TIME_FORMAT': '',
    'YEAR_MONTH_FORMAT': '',
    'MONTH_DAY_FORMAT': '',
    'SHORT_DATE_FORMAT': '',
    'SHORT_DATETIME_FORMAT': '',
}

for key in formats:
    formats[key] = get_format(key).replace('P', 'g:i a')
    
def date(val, arg=""):
    if not val:
        return _("Never")
    if not arg:
        arg = formats['DATE_FORMAT']
    elif arg in formats:
        arg = formats[arg]
    return format(localtime(val), arg)


def reldate(val, arg=""):
    if not val:
        return _("Never")
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
    if format(local, 'D') != format(local_now, 'D') and diff.days > -7 and diff.days < 7:
        return _("%(day)s, %(hour)s") % {'day': format(local, 'l'), 'hour': time_format(local, formats['TIME_FORMAT'])}

    # Fallback to date      
    return date(val, arg)


def reltimesince(val, arg=""):
    if not val:
        return _("Never")
    now = datetime.now(utc if is_aware(val) else None)
    diff = now - val
    local = localtime(val)

    # Difference is greater than day for sure
    if diff.days != 0:
        return reldate(val, arg)

    # Display specific time
    if diff.seconds >= 0:
        if diff.seconds <= 5:
            return _("Just now")
                        
        if diff.seconds < 3540:
            minutes = int(math.ceil(diff.seconds / 60.0))
            return ungettext(
                    "Minute ago",
                    "%(minutes)s minutes ago",
                minutes) % {'minutes': minutes}

        if diff.seconds < 3660:
            return _("Hour ago")
        
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
                
            return ungettext(
                    "Hour ago",
                    "%(hours)s hours ago",
                hours) % {'hours': hours}

    # Fallback to reldate
    return reldate(val, arg)


def compact(val):
    if not val:
        return _("Never")
    now = datetime.now(utc if is_aware(val) else None)
    local = localtime(val)

    if now.year == local.year:        
        return format(localtime(val), _('j M'))
    return format(localtime(val), _('j M y'))


def relcompact(val):
    if not val:
        return _("Never")
    now = datetime.now(utc if is_aware(val) else None)
    diff = now - val
    local = localtime(val)

    # Difference is greater than day for sure
    if diff.days != 0:
        return compact(val)

    if diff.seconds >= 0:
        if diff.seconds <= 60:
            return _("Now")
        if diff.seconds < 3600:
            minutes = int(math.ceil(diff.seconds / 60.0))
            return pgettext("number of minutes", "%(minute)sm") % {'minute': minutes}
        if diff.seconds < 86400:
            hours = int(math.ceil(diff.seconds / 3600.0))
            return pgettext("number of hours", "%(hour)sh") % {'hour': hours}

    return compact(val)