from django import template
from django.utils.translation import pgettext

register = template.Library()


@register.simple_tag
def pagetitle(title, **kwargs):
    if "page" in kwargs and kwargs["page"] > 1:
        title += " (%s)" % (
            pgettext("page title pagination", "page: %(page)s")
            % {"page": kwargs["page"]}
        )

    if "parent" in kwargs:
        title += " | %s" % kwargs["parent"]

    return title
