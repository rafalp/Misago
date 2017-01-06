from __future__ import unicode_literals

import re

from misago.core.pgutils import batch_update
from misago.threads.checksums import update_post_checksum
from misago.threads.models import Post

from . import fetch_assoc, movedids


def clean_posts():
    for post in batch_update(Post.objects):
        print '----' * 8
        post.original = clean_original(post.original)
        post.parsed = clean_parsed(post.parsed)

        # update_post_checksum(post)
        # post.save()


def clean_original(post):
    post = convert_quotes_to_bbcode(post)

    return post


def clean_parsed(post):
    post = update_quotes_markup(post)

    return post


def convert_quotes_to_bbcode(post):
    if not (post[0] == '>' or '\n>' in post):
        return post

    clean_lines = []

    in_quote = False
    quote_author = None
    quote = []

    for i, line in enumerate(post.splitlines() + ['']):
        if in_quote:
            if line.startswith('>'):
                quote.append(line[1:].lstrip())
            else:
                clean_lines.append('')
                if quote_author:
                    clean_lines.append('[quote="%s"]' % quote_author)
                clean_lines += quote
                clean_lines.append('[/quote]')
                clean_lines.append('')

                in_quote = False
                quote_author = None
                quote = []

                clean_lines.append(line)
        elif line.startswith('>'):
            in_quote = True

            if clean_lines and clean_lines[-1].startswith('@'):
                quote_author = clean_lines.pop(-1)

            quote.append(line[1:].lstrip())
        else:
            clean_lines.append(line)

    return convert_quotes_to_bbcode('\n'.join(clean_lines))


MD_QUOTE_RE = re.compile(r'''
<blockquote>(?P<content>.*?)</blockquote>
'''.strip(), re.IGNORECASE | re.MULTILINE | re.DOTALL);
MD_QUOTE_TITLE_RE = re.compile(r'''
<quotetitle>(?P<content>.*?)</quotetitle>
'''.strip(), re.IGNORECASE | re.MULTILINE | re.DOTALL);
MD_QUOTE_CONTENT_RE = re.compile(r'''
<article>(?P<content>.*?)</article>
'''.strip(), re.IGNORECASE | re.MULTILINE | re.DOTALL);


def update_quotes_markup(post):
    if not ('<blockquote>' in post and '<article>' in post):
        return post

    post = MD_QUOTE_RE.sub(replace_quote, post)

    return update_quotes_markup(post)


def replace_quote(matchobj):
    title_match = MD_QUOTE_TITLE_RE.search(matchobj.group('content'))
    content_match = MD_QUOTE_CONTENT_RE.search(matchobj.group('content'))

    if not (title_match and content_match):
        return matchobj.group('content')

    title = title_match.group('content')
    content = content_match.group('content')

    return '\n'.join([
        '<aside class="quote-block">',
        '<div class="quote-heading">%s</div>' % title,
        '<blockquote class="quote-body">',
        content.strip(),
        '</blockquote>',
        '</aside>',
    ])
