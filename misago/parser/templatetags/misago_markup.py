from django import template
from django.utils.safestring import mark_safe

from ..html import complete_markup_html

register = template.Library()


@register.simple_tag
def completemarkup(html: str, **kwargs):
    return mark_safe(complete_markup_html(html, **kwargs))
