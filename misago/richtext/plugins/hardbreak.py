HARD_BREAK_PATTERN = r"(\s+)?\n(\s+)?"


def parse_hard_break(self, m, state):
    return ("linebreak",)


def plugin_hard_break(md):
    md.inline.register_rule("hard_break", HARD_BREAK_PATTERN, parse_hard_break)
    md.inline.rules.append("hard_break")
