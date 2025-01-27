from django import template
from django.utils.safestring import mark_safe

from ..richtext import replace_rich_text_tokens

register = template.Library()


@register.simple_tag
def rich_text(html: str, data: dict | None = None):
    return mark_safe(replace_rich_text_tokens(html, data))
