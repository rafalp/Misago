from __future__ import unicode_literals

import re

from django.utils.translation import gettext as _


HEADER_RE = re.compile(r'''
<header>(?P<author>.*?)</header>
'''.strip(), re.IGNORECASE | re.MULTILINE | re.DOTALL);


def finalise_markup(post):
    return HEADER_RE.sub(replace_headers, post)


def replace_headers(matchobj):
    author = matchobj.group('author')
    if author:
        quote_title = _("%(author)s has written:") % {'author': author}
    else:
        quote_title = _("Quoted message:")
    return '<header>{}</header>'.format(quote_title)
