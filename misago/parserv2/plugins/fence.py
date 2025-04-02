# Copied from with changes
# https://github.com/executablebooks/markdown-it-py/blob/36a9d146af52265420de634cc2e25d1d40cfcdb7/markdown_it/rules_block/fence.py
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
from markdown_it.common.utils import escapeHtml
from markdown_it.renderer import RendererHTML
from markdown_it.rules_block.state_block import StateBlock
from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from ..codeargs import parse_code_args


def fence_plugin(md: MarkdownIt):
    md.block.ruler.at(
        "fence", fence_rule, {"alt": ["paragraph", "reference", "blockquote", "list"]}
    )
    md.add_render_rule("fence", render_fence_rule)


def fence_rule(state: StateBlock, startLine: int, endLine: int, silent: bool) -> bool:
    haveEndMarker = False
    pos = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]

    if state.is_code_block(startLine):
        return False

    if pos + 3 > maximum:
        return False

    marker = state.src[pos]

    if marker not in ("~", "`"):
        return False

    # scan marker length
    mem = pos
    pos = state.skipCharsStr(pos, marker)

    length = pos - mem

    if length < 3:
        return False

    markup = state.src[mem:pos]
    params = state.src[pos:maximum]

    if marker == "`" and marker in params:
        return False

    # Since start is found, we can report success here in validation mode
    if silent:
        return True

    # search end of block
    nextLine = startLine

    while True:
        nextLine += 1
        if nextLine >= endLine:
            # unclosed block should be autoclosed by end of document.
            # also block seems to be autoclosed by end of parent
            break

        pos = mem = state.bMarks[nextLine] + state.tShift[nextLine]
        maximum = state.eMarks[nextLine]

        if pos < maximum and state.sCount[nextLine] < state.blkIndent:
            # non-empty line with negative indent should stop the list:
            # - ```
            #  test
            break

        try:
            if state.src[pos] != marker:
                continue
        except IndexError:
            break

        if state.is_code_block(nextLine):
            continue

        pos = state.skipCharsStr(pos, marker)

        # closing code fence must be at least as long as the opening one
        if pos - mem < length:
            continue

        # make sure tail has spaces only
        pos = state.skipSpaces(pos)

        if pos < maximum:
            continue

        haveEndMarker = True
        # found!
        break

    # If a fence has heading spaces, they should be removed from its inner block
    length = state.sCount[startLine]

    state.line = nextLine + (1 if haveEndMarker else 0)

    token = state.push("fence", "code", 0)
    token.info = params
    token.content = state.getLines(startLine + 1, nextLine, length, True)
    token.markup = markup
    token.map = [startLine, state.line]

    if args_str := params.strip():
        args = parse_code_args(args_str)
        token.attrs = args
        token.info = args.get("info")

        if args.get("syntax"):
            token.meta["syntax"] = args["syntax"]

    return True


def render_fence_rule(
    renderer: RendererHTML,
    tokens: list[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
):
    token = tokens[idx]

    return (
        "<misago-code"
        + renderer.renderAttrs(token)
        + ">"
        + escapeHtml(token.content)
        + "</misago-code>\n"
    )
