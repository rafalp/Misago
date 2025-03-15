from markdown_it import MarkdownIt


def create_parser(context) -> MarkdownIt:
    md = MarkdownIt("js-default", {"typographer": True})
    md.enable(["replacements", "smartquotes"])
    return md
