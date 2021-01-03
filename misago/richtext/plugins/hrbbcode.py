import re

from mistune import Markdown


HR_BBCODE_PATTERN = re.compile(r"\[hr\]", re.IGNORECASE)


def parse_hr_bbcode(parser, m, state: dict):
    return {"type": "thematic_break", "blank": True}


def plugin_hr_bbcode(markdown: Markdown):
    markdown.block.register_rule("hr_bbcode", HR_BBCODE_PATTERN, parse_hr_bbcode)
    markdown.block.rules.append("hr_bbcode")
