from django import template
from django.conf import settings
from django.template.defaultfilters import date as dj_date
from django.utils import timezone


register = template.Library()


FORMAT_DAY_MONTH = settings.MISAGO_COMPACT_DATE_FORMAT_DAY_MONTH
FORMAT_DAY_MONTH_YEAR = settings.MISAGO_COMPACT_DATE_FORMAT_DAY_MONTH_YEAR


@register.filter
def compact_date(value):
    if value.year == timezone.now().year:
        return dj_date(value, FORMAT_DAY_MONTH)
    else:
        return dj_date(value, FORMAT_DAY_MONTH_YEAR)
