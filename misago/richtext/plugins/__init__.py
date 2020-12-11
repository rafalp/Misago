from mistune import PLUGINS

from .linebreaker import linebreaker
from .bbcode import bbcode

PLUGINS = PLUGINS.update({"simple_linebreak": linebreaker, "bbcode": bbcode})


__all__ = ["PLUGINS", "linebreaker", "bbcode"]
