from __future__ import unicode_literals


def convert_quotes_to_bbcode(post):
    if not (post[0] == '>' or '\n>' in post):
        return post

    clean_lines = []

    in_quote = False
    quote_author = None
    quote = []

    for line in post.splitlines() + ['']:
        if in_quote:
            if line.startswith('>'):
                quote.append(line[1:].lstrip())
            else:
                clean_lines.append('')

                if quote_author:
                    clean_lines.append('[quote="%s"]' % quote_author)
                else:
                    clean_lines.append('[quote]')

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
