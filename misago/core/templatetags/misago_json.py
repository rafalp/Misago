import json

from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def as_json(value):
    json_dump = json.dumps(value)
    # fixes XSS as described in #651
    return mark_safe(json_dump.replace('<', r'\u003C'))
