import re

from django.utils.translation import pgettext

QUOTE_HEADER_RE = re.compile(
    r"""
<div class="quote-heading" data-noquote="1">(?P<title>.*?)</div>
""".strip(),
    re.IGNORECASE | re.MULTILINE | re.DOTALL,
)

SPOILER_REVEAL_BTN = '<button class="spoiler-reveal" type="button"></button>'


def finalize_markup(post):
    post = QUOTE_HEADER_RE.sub(replace_quote_headers, post)
    post = replace_spoiler_reveal_buttons(post)
    return post


def replace_quote_headers(matchobj):
    title = matchobj.group("title")
    if title:
        quote_title = pgettext("quote title", "%(title)s has written:") % {
            "title": title
        }
    else:
        quote_title = pgettext("quote title", "Quoted message:")
    return '<div class="quote-heading" data-noquote="1">%s</div>' % quote_title


def replace_spoiler_reveal_buttons(post):
    final_btn = SPOILER_REVEAL_BTN.replace(
        "></", ">%s</" % pgettext("spoiler", "Reveal spoiler")
    )
    return post.replace(SPOILER_REVEAL_BTN, final_btn)
