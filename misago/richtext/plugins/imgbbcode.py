from mistune import Markdown
from mistune.inline_parser import escape_url

IMG_BBCODE_PATTERN = r"\[img(=(\"|')?(.*)(\"|')?)?\](.*)\[\/img\]"


def parse_img_bbcode(parser, m, state: dict):
    img_attr = m.group(3)
    img_or_alt = m.group(5)

    if img_attr:
        img = escape_url(img_attr)
        alt = img_or_alt
    else:
        img = escape_url(img_or_alt)
        alt = None

    return "image", img, alt, None


def plugin_img_bbcode(markdown: Markdown):
    markdown.inline.register_rule("img_bbcode", IMG_BBCODE_PATTERN, parse_img_bbcode)
    markdown.inline.rules.append("img_bbcode")
