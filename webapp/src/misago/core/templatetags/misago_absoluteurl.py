from django import template
from django.urls import NoReverseMatch, reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def absoluteurl(context, url_or_name, *args, **kwargs):
    address = context["settings"].forum_address
    if not address:
        return None

    absolute_url_prefix = address.rstrip("/")

    try:
        url_or_name = reverse(url_or_name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        # don't use URLValidator because its too explicit
        if not url_or_name.startswith("/"):
            return url_or_name

    return "%s%s" % (absolute_url_prefix, url_or_name)
