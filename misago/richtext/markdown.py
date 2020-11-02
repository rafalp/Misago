import mistune


class Renderer(mistune.HTMLRenderer):
    pass


def markdown(text, escape=True):
    plugins = ['url', 'strikethrough', 'footnotes', 'table', 'task_lists']
    md = mistune.create_markdown(escape, Renderer(), plugins)
    return md(text)
