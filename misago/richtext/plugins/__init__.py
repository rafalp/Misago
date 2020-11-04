from mistune import PLUGINS

from .linebreaker import linebreaker

PLUGINS = PLUGINS.update({'simple_linebreak': linebreaker})


__all__ = [
    'PLUGINS',
    'linebreaker'
]
