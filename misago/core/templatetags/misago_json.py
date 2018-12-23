import json

from django import template
from django.utils.safestring import mark_safe

from ..utils import encode_json_html

register = template.Library()


@register.filter
def as_json(value):
    json_dump = json.dumps(value)
    # fixes XSS as described in #651
    return mark_safe(encode_json_html(json_dump))
