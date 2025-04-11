from django import template
from django.template import Context
from django.utils.safestring import mark_safe

from ...threads.models import Thread
from ..richtext import replace_rich_text_tokens

register = template.Library()


@register.simple_tag(takes_context=True)
def rich_text(
    context: Context,
    html: str,
    data: dict | None = None,
    *,
    thread: Thread | None = None,
):
    return mark_safe(replace_rich_text_tokens(html, context, data, thread))
