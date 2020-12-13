__all__ = [
    "color",
    "size",
]


COLOR = r'\[color="((\w)*)"\](.*)\[\/color\]'
SIZE = r"\[size=((\d)*)\](.*)\[\/size\]"


def color_parser(parser, m, state):
    text_color = m.group(1)
    children = parser(m.group(3), state)
    return "color", {"children": children, "color": text_color}


def size_parser(parser, m, state):
    text_size = m.group(1)
    children = parser(m.group(3), state)
    return "size", {"children": children, "size": text_size}


def color(md):
    md.inline.register_rule("color", COLOR, color_parser)
    md.inline.rules.append("color")


def size(md):
    md.inline.register_rule("size", SIZE, size_parser)
    md.inline.rules.append("size")
