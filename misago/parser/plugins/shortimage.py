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

from markdown_it import MarkdownIt
from markdown_it.common.utils import isStrSpace
from markdown_it.rules_inline.state_inline import StateInline
from markdown_it.token import Token


def short_image_plugin(md: MarkdownIt):
    md.inline.ruler.after("image", "short_image", short_image_rule)


def short_image_rule(state: StateInline, silent: bool):
    title = ""
    href = ""

    imageStart = state.pos
    max = state.posMax

    if state.src[state.pos] != "!":
        return False

    pos = imageStart + 1

    if pos >= max or state.src[pos] != "(":
        return False

    # [link](  <href>  "title"  )
    #        ^^ skipping these spaces
    pos += 1
    while pos < max:
        ch = state.src[pos]
        if not isStrSpace(ch) and ch != "\n":
            break
        pos += 1

    if pos >= max:
        return False

    # [link](  <href>  "title"  )
    #          ^^^^^^ parsing link destination
    start = pos
    res = state.md.helpers.parseLinkDestination(state.src, pos, state.posMax)
    if res.ok:
        href = state.md.normalizeLink(res.str)
        if state.md.validateLink(href):
            pos = res.pos
        else:
            href = ""

    # [link](  <href>  "title"  )
    #                ^^ skipping these spaces
    start = pos
    while pos < max:
        ch = state.src[pos]
        if not isStrSpace(ch) and ch != "\n":
            break
        pos += 1

    # [link](  <href>  "title"  )
    #                  ^^^^^^^ parsing link title
    res = state.md.helpers.parseLinkTitle(state.src, pos, state.posMax)
    if pos < max and start != pos and res.ok:
        title = res.str
        pos = res.pos

        # [link](  <href>  "title"  )
        #                         ^^ skipping these spaces
        while pos < max:
            ch = state.src[pos]
            if not isStrSpace(ch) and ch != "\n":
                break
            pos += 1
    else:
        title = ""

    if pos >= max or state.src[pos] != ")" or not href:
        return False

    pos += 1

    if not silent:
        token = state.push("image", "img", 0)
        token.attrs = {"src": href, "alt": ""}
        token.children = None
        token.content = ""

        if title:
            token.attrSet("title", title)

    state.pos = pos
    state.posMax = max
    return True
