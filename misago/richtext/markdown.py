import mistune

from .ast_renderer import MisagoAstRenderer

PLUGINS = [
    "url",
    "strikethrough",
    "footnotes",
    "table",
    "task_lists",
    "simple_linebreak",
]


def ast_markdown(text, escape=True):
    md = mistune.create_markdown(escape, MisagoAstRenderer(), PLUGINS)
    return md(text)


def html_markdown(text, escape=True):
    md = mistune.create_markdown(escape, mistune.HTMLRenderer(), PLUGINS)
    return md(text)
