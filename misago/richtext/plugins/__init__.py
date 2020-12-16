from mistune import PLUGINS

from .linebreaker import linebreaker
from .bbcode import bbcode

PLUGINS.update({"simple_linebreak": linebreaker, "bbcode": bbcode})
default_plugins = [linebreaker, bbcode]

__all__ = ["default_plugins", "linebreaker", "bbcode"]
