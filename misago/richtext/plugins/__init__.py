from mistune.plugins import PLUGINS

from .bbcode import bbcode
from .hardbreak import plugin_hard_break
from .linebreaker import linebreaker
from .shortimage import plugin_short_image


PLUGINS.update({"simple_linebreak": linebreaker, "bbcode": bbcode})
default_plugins = [linebreaker, bbcode]

__all__ = ["default_plugins", "linebreaker", "bbcode"]

