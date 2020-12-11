from pprint import pprint
from mistune import PLUGINS

import mistune


from mistune.inline_parser import ESCAPE, PUNCTUATION

print(ESCAPE)


ITALIC = r'\[i\]((?:\\~|[^~])*(?:' + ESCAPE + r'|[^\s~]))\[\/i\]'
UNDERLINE = r'\[u\]((?:\\~|[^~])*(?:' + ESCAPE + r'|[^\s~]))\[\/u\]'
# BOLD = r'\[b\]((?:\\~|[^~])*(?:' + ESCAPE + r'|[^\s~]))\[\/b\]'
BOLD = r'\[b\](.*)\[\/b\]'
QUOTE = r'\[quote(="((\w)*)")?\](.*)\[\/quote\]'

UNDERSCORE_EMPHASIS = (
    r'\b(_{1,2})(?=[^\s_])([\s\S]*?'
    r'(?:' + ESCAPE + r'|[^\s_]))\1'
    r'(?!_|[^\s' + PUNCTUATION + r'])\b'
)

# BOLD = r'\[b\].*\[\/b\]'
# BOLD = r'.*b.*'
# BOLD = "alamakota"


def quote(parser, m, state):
    author = m.group(2)
    state['author'] = author
    text = m.group(4)
    result = parser(text, state)
    return "quote", {'res': result, 'author': author}


def bold(parser, m, state):
    print('===========================+++++=====================')
    print(f'{parser = }')
    print(f'{m = }')
    print(f'{state = }')
    return "strong", parser(m.group(1), state)


def italic(parser, m, state):
    """
    emphasized
    """
    return "emphasis", parser(m.group(0)[3:-4], state)


def underline(parser, m, state):
    return "underline", parser(m.group(0)[3:-4], state)


def bbcode(md):
    # md.inline.rules.remove('ref_link2')
    md.inline.register_rule("bbcode_bold", BOLD, bold)
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    md.inline.rules.insert(2, "bbcode_bold")

    md.inline.register_rule("bbcode_italic", ITALIC, italic)
    md.inline.rules.insert(3, "bbcode_italic")

    md.inline.register_rule("bbcode_underline", UNDERLINE, underline)
    md.inline.rules.insert(4, "bbcode_underline")

    md.inline.register_rule("bbcode_quote", QUOTE, quote)
    md.inline.rules.insert(4, "bbcode_quote")
    print(md.inline.rules)


# my_text = "Napiszę sobie coś [b]ważne[/b] i nie istone"
# my_text = "[abc]To jest a[/abc]"
# my_text = "Poczatek [b]xyz[/b] alamakota i psa"
# my_text = "Amo [b][i]Teraz[/i][/b] koniec"
# my_text = "Amo [u][b][i]Teraz[/i][/b][/u] koniec"
my_text = 'To [quote="Cyceron"]Jestem[/quote] albo byłem.'

PLUGINS["bbcode"] = bbcode


def ast_markdown(text, escape=True):
    md = mistune.create_markdown(escape, mistune.AstRenderer(), PLUGINS)
    return md(text)


res = ast_markdown(my_text)

pprint(res)

