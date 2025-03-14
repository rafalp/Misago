import html

from django.conf import settings
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

from .hooks import highlight_syntax_hook


def highlight_syntax(syntax: str, code: str) -> str:
    return highlight_syntax_hook(_highlight_syntax_action, syntax, code)


def _highlight_syntax_action(syntax: str, code: str) -> str:
    try:
        # Check if lexer exists
        get_lexer_by_name(syntax)
    except ClassNotFound:
        return html.escape(code)

    lexer = get_lexer_by_name(syntax, stripall=True)

    formatter = MisagoHtmlFormatter(
        style=settings.MISAGO_PYGMENTS_STYLE,
        noclasses=True,
    )

    return highlight(code, lexer, formatter)


class MisagoHtmlFormatter(HtmlFormatter):
    """Custom HTML formatter that excludes `<pre><code><div>` from the result"""

    def _wrap_div(self, inner):
        yield from inner

    def _wrap_pre(self, inner):
        # the empty span here is to keep leading empty lines from being
        # ignored by HTML parsers
        yield 0, ("<span></span>")
        yield from inner
