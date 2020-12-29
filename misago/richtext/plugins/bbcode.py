__all__ = [
    "bbcode",
]

BOLD = r"\[b\](.*)\[\/b\]"
ITALIC = r"\[i\](.*)\[\/i\]"
UNDERLINE = r"\[u\](.*)\[\/u\]"
LINE_THROUGH = r"\[s\](.*)\[\/s\]"
CENTER = r"\[center\](.*)\[\/center\]"
QUOTE = r'\[quote(=(@([\w\-_]*))(:\d+)?)?\](.*)\[\/quote\]'
BLOCK_CODE = r"\[code\](.*)\[\/code\]"
LINK = r"\[url=(.*)\](.*)\[\/url\]"
LIST_START = r"\[(\/)?list\]"
LIST_ITEM = r"\[\*\](.*)\n"
IMG_LONG = r"\[img\](.*)\[\/img\]"
IMG_SHORT = r"\[img=([^\]]*)\]"


def bold(parser, m, state):
    return "strong", parser(m.group(1), state)


def italic(parser, m, state):
    """
    emphasized
    """
    return "emphasis", parser(m.group(1), state)


def underline(parser, m, state):
    return "underline", parser(m.group(1), state)


def line_through(parser, m, state):
    return "line_through", parser(m.group(1), state)


def center(parser, m, state):
    return "center", parser(m.group(1), state)


def quote(parser, m, state):
    return "quote", {"author": m.group(3), "id_post": m.group(4), "children": parser(m.group(5), state)}


def block_code(parser, m, state):
    return "block_code", parser(m.group(1), state)


def link_parser(parser, m, state):
    title = m.group(2)
    return "link", m.group(1), parser(title, state), title


def list_parser(parser, m, state):
    if m.group(1):
        # found [/list] - tag end of list
        return "list_end", None
    return "list_start", None


def list_item(parser, m, state):
    return "list_item", parser(m.group(1), state), 0


def img_both(parser, m, state):
    return "image", m.group(1)


def bbcode(md):
    md.inline.register_rule("bbcode_bold", BOLD, bold)
    md.inline.rules.insert(2, "bbcode_bold")

    md.inline.register_rule("bbcode_italic", ITALIC, italic)
    md.inline.rules.insert(3, "bbcode_italic")

    md.inline.register_rule("bbcode_underline", UNDERLINE, underline)
    md.inline.rules.insert(4, "bbcode_underline")

    md.inline.register_rule("bbcode_line_through", LINE_THROUGH, line_through)
    md.inline.rules.insert(5, "bbcode_line_through")

    md.inline.register_rule("bbcode_center", CENTER, center)
    md.inline.rules.insert(6, "bbcode_center")

    md.inline.register_rule("bbcode_quote", QUOTE, quote)
    md.inline.rules.insert(7, "bbcode_quote")

    md.inline.register_rule("bbcode_block_code", BLOCK_CODE, block_code)
    md.inline.rules.insert(8, "bbcode_block_code")

    md.inline.register_rule("bbcode_link2", LINK, link_parser)
    md.inline.rules.insert(9, "bbcode_link2")

    md.inline.register_rule("bbcode_list2", LIST_START, list_parser)
    md.inline.rules.insert(10, "bbcode_list2")

    md.inline.register_rule("bbcode_list2_item", LIST_ITEM, list_item)
    md.inline.rules.insert(11, "bbcode_list2_item")

    md.inline.register_rule("bbcode_img_long", IMG_LONG, img_both)
    md.inline.rules.insert(12, "bbcode_img_long")

    md.inline.register_rule("bbcode_img_short", IMG_SHORT, img_both)
    md.inline.rules.insert(13, "bbcode_img_short")
