from .codebbcode import plugin_code_bbcode
from .formattingbbcode import (
    plugin_bold_bbcode,
    plugin_italic_bbcode,
    plugin_strikethrough_bbcode,
    plugin_subscript_bbcode,
    plugin_superscript_bbcode,
    plugin_underline_bbcode,
)
from .genericblock import plugin_generic_block
from .hardbreak import plugin_hard_break
from .hrbbcode import plugin_hr_bbcode
from .imgbbcode import plugin_img_bbcode
from .mention import plugion_mention
from .quotebbcode import plugin_quote_bbcode
from .shortimage import plugin_short_image
from .spoilerbbcode import plugin_spoiler_bbcode
from .url import plugin_url
from .urlbbcode import plugin_url_bbcode


builtin_plugins = [
    plugin_bold_bbcode,
    plugin_code_bbcode,
    plugin_generic_block,
    plugin_hard_break,
    plugin_hr_bbcode,
    plugin_img_bbcode,
    plugin_italic_bbcode,
    plugion_mention,
    plugin_short_image,
    plugin_strikethrough_bbcode,
    plugin_subscript_bbcode,
    plugin_superscript_bbcode,
    plugin_quote_bbcode,
    plugin_spoiler_bbcode,
    plugin_underline_bbcode,
    plugin_url,
    plugin_url_bbcode,
]
