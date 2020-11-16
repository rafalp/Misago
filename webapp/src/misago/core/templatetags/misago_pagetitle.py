from django import template
from django.utils.translation import gettext as _

register = template.Library()


@register.simple_tag
def pagetitle(title, **kwargs):
    if "page" in kwargs and kwargs["page"] > 1:
        title += " (%s)" % (_("page: %(page)s") % {"page": kwargs["page"]})

    if "parent" in kwargs:
        title += " | %s" % kwargs["parent"]

    return title
