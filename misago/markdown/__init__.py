from mistune import create_markdown
from .renderers import Renderer


def markdown(text, escape=True):
    plugins = ['url', 'strikethrough', 'footnotes', 'table', 'task_lists']
    md = create_markdown(escape, Renderer(), plugins)
    return md(text)


__all__ = [
    'markdown',
]
