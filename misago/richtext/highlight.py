from html import escape
from typing import List, Optional

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound


def highlight_code(code: str, syntax: Optional[str] = None) -> str:
    code = trim_code(code)
    code = reset_indentation(code)
    if syntax:
        try:
            lexer = get_lexer_by_name(syntax, stripall=True)
            formatter = MisagoHtmlFormatter(classprefix="hl-")
            return (
                highlight(code, lexer, formatter).replace("<span></span>", "").strip()
            )
        except ClassNotFound:
            pass

    return escape(code)


def trim_code(code: str) -> str:
    lines: List[str] = []
    for line in code.splitlines():
        if lines or line.strip():
            lines.append(line)

    return "\n".join(lines).rstrip()


def reset_indentation(code: str) -> str:
    min_indent = None
    for line in code.splitlines():
        indent = len(line) - len(line.lstrip())
        if min_indent is None or indent < min_indent:
            min_indent = indent

    if not min_indent:
        return code

    lines: List[str] = []
    for line in code.splitlines():
        if line.strip():
            lines.append(line[min_indent:])
        else:
            lines.append("")

    return "\n".join(lines)


class MisagoHtmlFormatter(HtmlFormatter):
    def wrap(self, source, outfile):
        yield from source
