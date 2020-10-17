__all__ = [
    "linebreaker",
]


LINEBREAK = r"\n(?!\s*$)"


def break_line(inline_parser, m, state):
    return ("linebreak",)


def linebreaker(md):
    md.inline.register_rule("simple_linebreak", LINEBREAK, break_line)
    md.inline.rules.append("simple_linebreak")
