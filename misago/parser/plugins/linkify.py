# Copied from with changes
# https://github.com/executablebooks/markdown-it-py/blob/36a9d146af52265420de634cc2e25d1d40cfcdb7/markdown_it/rules_inline/linkify.py
#
# MIT License

# Copyright (c) 2020 ExecutableBookProject

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re

from markdown_it import MarkdownIt
from markdown_it.rules_inline.state_inline import StateInline

# RFC3986: scheme = ALPHA *( ALPHA / DIGIT / "+" / "-" / "." )
SCHEME_RE = re.compile(r"(?:^|[^a-z0-9.+-])([a-z][a-z0-9.+-]*)$", re.IGNORECASE)


def linkify_plugin(md: MarkdownIt):
    md.inline.ruler.at("linkify", linkify_rule)


def linkify_rule(state: StateInline, silent: bool) -> bool:
    """Rule for identifying plain-text links."""
    if not state.md.options.linkify:
        return False
    if state.linkLevel > 0:
        return False
    if not state.md.linkify:
        raise ModuleNotFoundError("Linkify enabled but not installed.")

    pos = state.pos
    maximum = state.posMax

    if (
        (pos + 3) > maximum
        or state.src[pos] != ":"
        or state.src[pos + 1] != "/"
        or state.src[pos + 2] != "/"
    ):
        return False

    if not (match := SCHEME_RE.search(state.pending)):
        return False

    proto = match.group(1)
    if not (
        link := state.md.linkify.match_at_start(state.src[pos - len(proto) : maximum])
    ):
        return False
    url: str = link.url

    # disallow '*' at the end of the link (conflicts with emphasis)
    url = url.rstrip("*")

    full_url = state.md.normalizeLink(url)
    if not state.md.validateLink(full_url):
        return False

    if not silent:
        state.pending = state.pending[: -len(proto)]

        token = state.push("link_open", "a", 1)
        token.attrs = {"href": full_url}
        token.markup = "linkify"
        token.info = "auto"

        token = state.push("text", "", 0)
        token.content = state.md.normalizeLinkText(url)

        token = state.push("link_close", "a", -1)
        token.markup = "linkify"
        token.info = "auto"

    state.pos += len(url) - len(proto)
    return True
