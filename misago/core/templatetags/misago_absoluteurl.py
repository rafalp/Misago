from django import template
from django.urls import NoReverseMatch, reverse

from misago.conf import settings

register = template.Library()


@register.simple_tag
def absoluteurl(url_or_name, *args, **kwargs):
    if not settings.MISAGO_ADDRESS:
        return None

    absolute_url_prefix = settings.MISAGO_ADDRESS.rstrip('/')

    try:
        url_or_name = reverse(url_or_name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        # don't use URLValidator because its too explicit
        if not url_or_name.startswith('/'):
            return url_or_name
    
    return u'{}{}'.format(absolute_url_prefix, url_or_name)