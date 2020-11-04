import mistune

PLUGINS = ['url', 'strikethrough', 'footnotes', 'table', 'task_lists']


def asr_markdown(text, escape=True):
    md = mistune.create_markdown(escape, mistune.AstRenderer(), PLUGINS)
    return md(text)


def html_markdown(text, escape=True):
    md = mistune.create_markdown(escape, mistune.HTMLRenderer(), PLUGINS)
    return md(text)
