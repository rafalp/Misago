from django import template

from ..daterelative import (
    date_relative,
    date_relative_in_sentence,
    date_relative_short,
)

register = template.Library()

register.filter(is_safe=False, expects_localtime=True)(date_relative)
register.filter(is_safe=False, expects_localtime=True)(date_relative_in_sentence)
register.filter(is_safe=False, expects_localtime=True)(date_relative_short)
