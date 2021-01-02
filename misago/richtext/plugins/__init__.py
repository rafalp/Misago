from .codebbcode import plugin_code_bbcode
from .genericblock import plugin_generic_block
from .hardbreak import plugin_hard_break
from .quotebbcode import plugin_quote_bbcode
from .shortimage import plugin_short_image
from .spoilerbbcode import plugin_spoiler_bbcode


builtin_plugins = [
    plugin_code_bbcode,
    plugin_generic_block,
    plugin_hard_break,
    plugin_short_image,
    plugin_quote_bbcode,
    plugin_spoiler_bbcode,
]
