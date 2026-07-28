from django import template
from django.utils.safestring import mark_safe

from ..daterelative import (
    date_relative,
    date_relative_in_sentence,
    date_relative_short,
)

register = template.Library()

register.filter(is_safe=False, expects_localtime=True)(date_relative)
register.filter(is_safe=False, expects_localtime=True)(date_relative_in_sentence)
register.filter(is_safe=False, expects_localtime=True)(date_relative_short)


@register.simple_tag
def safestrformat(value, **kwargs):
    try:
        return mark_safe(value % kwargs)
    except (TypeError, ValueError, KeyError):
        return mark_safe(value)
