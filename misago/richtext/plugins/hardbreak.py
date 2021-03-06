from mistune import Markdown

HARD_BREAK_PATTERN = r"(\s+)?\n(\s+)?"


def parse_hard_break(parser, m, state: dict):
    return ("linebreak",)


def plugin_hard_break(markdown: Markdown):
    markdown.inline.register_rule("hard_break", HARD_BREAK_PATTERN, parse_hard_break)
    markdown.inline.rules.append("hard_break")
