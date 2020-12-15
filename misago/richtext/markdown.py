import mistune

from .html_renderer import MisagoHTMLRenderer


PLUGINS = [
    "bbcode",
    "url",
    "strikethrough",
    "footnotes",
    "table",
    "task_lists",
    "simple_linebreak",
]


def ast_markdown(text, escape=True):
    md = mistune.create_markdown(escape, mistune.AstRenderer(), PLUGINS)
    return md(text)


def html_markdown(text, escape=True):
    md = mistune.create_markdown(escape, MisagoHTMLRenderer(), PLUGINS)
    return md(text)
