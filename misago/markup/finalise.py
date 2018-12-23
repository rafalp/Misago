import re

from django.utils.translation import gettext as _

HEADER_RE = re.compile(
    r"""
<div class="quote-heading">(?P<title>.*?)</div>
""".strip(),
    re.IGNORECASE | re.MULTILINE | re.DOTALL,
)


def finalise_markup(post):
    return HEADER_RE.sub(replace_headers, post)


def replace_headers(matchobj):
    title = matchobj.group("title")
    if title:
        quote_title = _("%(title)s has written:") % {"title": title}
    else:
        quote_title = _("Quoted message:")
    return '<div class="quote-heading">%s</div>' % quote_title
