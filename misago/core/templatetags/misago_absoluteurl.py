from django import template
from django.urls import reverse

from misago.conf import settings

register = template.Library()


@register.simple_tag
def absoluteurl(url_or_name, *args, **kwargs):
    if not settings.MISAGO_ADDRESS:
        return None

    absolute_url_prefix = settings.MISAGO_ADDRESS.rstrip('/')

    if '/' not in url_or_name:
        url_or_name = reverse(url_or_name, args=args, kwargs=kwargs)
    
    return u'{}{}'.format(absolute_url_prefix, url_or_name)