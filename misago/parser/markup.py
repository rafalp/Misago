from dataclasses import dataclass
from textwrap import dedent, indent
from typing import Callable

from markdown_it.renderer import RendererProtocol
from markdown_it.token import Token

from .escape import escape
from .hooks import render_tokens_to_markup_hook


RendererMarkupRule = Callable[["StateMarkup"], bool]


@dataclass
class StateMarkup:
    renderer: "RendererMarkup"
    tokens: list[Token]
    pos: int
    posMax: int
    list_item_prefix: str
    nesting: int | None = None
    result: str = ""

    def push_block(self, text: str, nesting: int = 0):
        if self.result and self.nesting is not None:
            if nesting >= 0:
                if self.nesting == 1:
                    self.result += "\n"
                else:
                    self.result += "\n\n"
            else:
                self.result += "\n"

        self.result += text
        self.nesting = nesting

    def push(self, text: str, softbreak: bool = False):
        if self.result and softbreak:
            self.result += "\n"

        self.result += text

    def push_softbreak(self):
        if self.result:
            self.result += "\n"


class RendererMarkup(RendererProtocol):
    __output__ = "text"

    rules: list[RendererMarkupRule]

    def __init__(self, rules: list[RendererMarkupRule]):
        self.rules = rules

    def render(self, tokens: list[Token], list_item_prefix: str | None = None) -> str:
        state = StateMarkup(
            renderer=self,
            tokens=tokens,
            pos=0,
            posMax=len(tokens) - 1,
            list_item_prefix=list_item_prefix,
        )

        while state.pos <= state.posMax:
            for rule in self.rules:
                if rule(state):
                    break
            else:
                state.pos += 1

        return state.result.strip()


def render_tokens_to_markup(tokens: list[Token]) -> str:
    return render_tokens_to_markup_hook(
        _render_tokens_to_markup_action,
        tokens,
        [
            render_header,
            render_code_block,
            render_code_fence,
            render_code_bbcode,
            render_quote_bbcode,
            # render_spoiler_bbcode,
            # render_ordered_list,
            # render_bullet_list,
            # render_table,
            # render_attachment,
            render_paragraph,
            render_inline,
            # render_code_inline,
            # render_mention,
            # render_link,
            # render_image,
            # render_video,
            render_softbreak,
            render_text,
        ],
    )


def _render_tokens_to_markup_action(
    tokens: list[Token],
    rules: list[tuple[str, RendererMarkupRule]],
) -> str:
    renderer = RendererMarkup(rules)
    return renderer.render(tokens)


def render_header(state: StateMarkup) -> bool:
    match = match_token_pair(state, "heading_open", "heading_close")
    if not match:
        return False

    tokens, pos = match
    heading_open = tokens[0]

    if heading_open.markup[0] == "#":
        state.push_block(f"{heading_open.markup} ")
        state.push(state.renderer.render(tokens[1:-1]))
    else:
        state.push_block(state.renderer.render(tokens[1:-1]))
        state.push_softbreak()
        state.push(heading_open.markup * 5)

    state.pos = pos

    return True


def render_code_block(state: StateMarkup) -> bool:
    token = state.tokens[state.pos]
    if token.type != "code_block":
        return False

    content = dedent(token.content).rstrip()
    state.push_block(indent(content, "    "))

    state.pos += 1
    return True


def render_code_fence(state: StateMarkup) -> bool:
    token = state.tokens[state.pos]
    if token.type != "fence":
        return False

    info = token.attrs.get("info")
    syntax = token.attrs.get("syntax")
    content = dedent(token.content).rstrip()

    args = None
    if info and syntax:
        args = f"{escape(info)}, syntax: {escape(syntax)}"
    elif info or syntax:
        args = escape(info or syntax)

    if args:
        state.push_block(f"{token.markup}{args}", nesting=1)
    else:
        state.push_block(token.markup, nesting=1)

    state.push_block(content)
    state.push_block(token.markup, nesting=-1)

    state.pos += 1
    return True


def render_code_bbcode(state: StateMarkup) -> bool:
    token = state.tokens[state.pos]
    if token.type != "code_bbcode":
        return False

    info = token.attrs.get("info")
    syntax = token.attrs.get("syntax")
    content = dedent(token.content).rstrip()

    args = None
    if info and syntax:
        args = f"{escape(info, '[]')}, syntax: {escape(syntax, '[]')}"
    elif info or syntax:
        args = escape(info or syntax, "[]")

    if args:
        if '"' in args:
            args = f'"{args}"'

        state.push_block(f"[code={args}]", nesting=1)
    else:
        state.push_block("[code]", nesting=1)

    state.push_block(content)
    state.push_block("[/code]", nesting=-1)

    state.pos += 1
    return True


def render_quote_bbcode(state: StateMarkup) -> bool:
    match = match_token_pair(state, "quote_bbcode_open", "quote_bbcode_close")
    if not match:
        return False

    tokens, pos = match
    opening_token = tokens[0]

    info = opening_token.attrs.get("info")
    user = opening_token.attrs.get("user")
    post = opening_token.attrs.get("post")

    args = None
    if user and post:
        args = f"{user}, post: {post}"
    elif info:
        args = info

    if args:
        if '"' in args:
            args = f'"{escape(args, '[]')}"'

        state.push_block(f"[quote={args}]", nesting=1)
    else:
        state.push_block("[quote]", nesting=1)

    state.push_block(state.renderer.render(tokens[1:-1]))
    state.push_block("[/quote]", nesting=-1)
    state.pos = pos

    return True


def render_spoiler_bbcode(state: StateMarkup) -> bool:
    match = match_token_pair(state, "spoiler_bbcode_open", "spoiler_bbcode_close")
    if not match:
        return False

    tokens, pos = match
    opening_token = tokens[0]

    if info := opening_token.attrs.get("info"):
        prefix = f"{info}:\n"
    else:
        prefix = ""

    state.push(prefix + state.renderer.render(tokens[1:-1]), hardbreak=True)
    state.pos = pos

    return True


def render_ordered_list(state: StateMarkup) -> bool:
    match = match_token_pair(state, "ordered_list_open", "ordered_list_close")
    if not match:
        return False

    tokens, pos = match
    content = render_list_content(state, tokens)

    if state.list_item_prefix:
        content = "\n" + content
    else:
        content = "\n\n" + content

    state.push(content)
    state.pos = pos
    return True


def render_bullet_list(state: StateMarkup) -> bool:
    match = match_token_pair(state, "bullet_list_open", "bullet_list_close")
    if not match:
        return False

    tokens, pos = match
    content = render_list_content(state, tokens)

    if state.list_item_prefix:
        content = "\n" + content
    else:
        content = "\n\n" + content

    state.push(content)
    state.pos = pos
    return True


def render_list_content(
    state: StateMarkup, tokens: list[Token], prefix: str | None = None
) -> str:
    prefix = prefix or state.list_item_prefix or ""

    opening_token = tokens[0]
    is_ordered = opening_token.type == "ordered_list_open"

    if is_ordered:
        start = opening_token.attrs.get("start") or 1
    else:
        delimiter = opening_token.markup

    nesting_item = 0
    nesting_list = 0

    list_items: list[list[Token]] = []
    item_tokens: list[Token] = []
    for token in tokens[1:-1]:
        if token.type in ("ordered_list_open", "bullet_list_open"):
            nesting_list += 1
            item_tokens.append(token)
        elif token.type in ("ordered_list_close", "bullet_list_close"):
            nesting_list -= 1
            item_tokens.append(token)
        elif token.type == "list_item_open":
            nesting_item += 1
            if nesting_list:
                item_tokens.append(token)
        elif token.type == "list_item_close":
            nesting_item -= 1
            if not nesting_item and not nesting_list:
                list_items.append(item_tokens)
                item_tokens = []
            if nesting_list:
                item_tokens.append(token)
        elif nesting_item:
            item_tokens.append(token)

    rendered_items: list[str] = []
    for index, item_tokens in enumerate(list_items):
        if is_ordered:
            item_prefix = f"{prefix}{start + index}. "
        else:
            item_prefix = f"{prefix}{delimiter} "

        item_str = item_prefix
        item_str += state.renderer.render(item_tokens, item_prefix).strip()

        rendered_items.append(item_str.strip())

    return "\n".join(rendered_items)


def render_table(state: StateMarkup) -> bool:
    match = match_token_pair(state, "table_open", "table_close")
    if not match:
        return False

    tokens, pos = match

    table_rows: list[str] = []
    row_cells: list[str] = []
    cell_tokens: list[Token] = []

    nesting = 0

    for token in tokens[1:-1]:
        if token.type == "tr_close":
            table_rows.append(", ".join(row_cells))
            row_cells = []
        elif token.type in ("th_open", "td_open"):
            nesting += 1
        elif token.type in ("th_close", "td_close"):
            nesting -= 1
            if not nesting:
                row_cells.append(state.renderer.render(cell_tokens).strip())
                cell_tokens = []
        elif nesting:
            cell_tokens.append(token)

    state.push("\n".join(table_rows), hardbreak=True)
    state.pos = pos
    return True


def render_attachment(state: StateMarkup) -> bool:
    token = state.tokens[state.pos]
    if token.type != "attachment":
        return False

    use_hardbreak = True
    if state.pos:
        cursor = 0
        while cursor < state.pos:
            if state.tokens[cursor].type == "selection_boundary_close":
                cursor += 1
            else:
                if state.tokens[cursor].type == "attachment":
                    use_hardbreak = False
                elif state.tokens[cursor].nesting != 1:
                    use_hardbreak = True

                cursor += 1

    name = token.attrs.get("name")
    id = token.attrs.get("id")

    if name and id:
        state.push(
            f"<attachment={name}:{id}>",
            hardbreak=use_hardbreak,
            softbreak=not use_hardbreak,
        )

    state.pos += 1
    return True


def render_paragraph(state: StateMarkup) -> bool:
    match = match_token_pair(state, "paragraph_open", "paragraph_close")
    if not match:
        return False

    tokens, pos = match

    state.push_block(state.renderer.render(tokens[1:-1]), nesting=0)
    state.pos = pos

    return True


def render_inline(state: StateMarkup) -> bool:
    token = state.tokens[state.pos]
    if token.type != "inline":
        return False

    state.push(state.renderer.render(token.children))
    state.pos += 1
    return True


def render_code_inline(state: StateMarkup) -> bool:
    token = state.tokens[state.pos]
    if token.type != "code_inline":
        return False

    state.push(token.content)
    state.pos += 1
    return True


def render_link(state: StateMarkup) -> bool:
    match = match_token_pair(state, "link_open", "link_close")
    if not match:
        return False

    tokens, pos = match
    opening_token = tokens[0]

    url = opening_token.attrs.get("href")

    state.push(url)

    if opening_token.info != "auto":
        if content := state.renderer.render(tokens[1:-1]).strip():
            state.push(f" ({content})")

    state.pos = pos
    return True


def render_image(state: StateMarkup) -> bool:
    token = state.tokens[state.pos]
    if token.type != "image":
        return False

    state.push(token.attrs["src"])

    alt = token.content
    title = token.attrs.get("title")

    if alt and title:
        state.push(f" ({alt}, {title})")
    elif alt:
        state.push(f" ({alt})")

    state.pos += 1
    return True


def render_video(state: StateMarkup) -> bool:
    token = state.tokens[state.pos]
    if token.type != "video":
        return False

    state.push(token.attrs["href"])
    state.pos += 1
    return True


def render_mention(state: StateMarkup) -> bool:
    match = match_token_pair(state, "link_open", "link_close")
    if not match:
        return False

    tokens, pos = match
    if not tokens[0].meta.get("mention"):
        return False

    state.push(state.renderer.render(tokens[1:-1]))
    state.pos = pos
    return True


def render_softbreak(state: StateMarkup) -> bool:
    token = state.tokens[state.pos]
    if token.type != "softbreak":
        return False

    state.push("\n")
    state.pos += 1
    return True


def render_text(state: StateMarkup) -> bool:
    token = state.tokens[state.pos]
    if token.type != "text":
        return False

    state.push(token.content)
    state.pos += 1
    return True


def match_token_pair(
    state: StateMarkup, type_open: str, type_close: str
) -> tuple[list[Token], int] | None:
    pos = state.pos
    nesting = 0
    tokens: list[Token] = []

    if state.tokens[pos].type != type_open:
        return None

    while pos <= state.posMax:
        tokens.append(state.tokens[pos])
        if state.tokens[pos].type == type_open:
            nesting += 1
        if state.tokens[pos].type == type_close:
            nesting -= 1
            if not nesting:
                break
        pos += 1

    if pos > state.posMax:
        return None

    return tokens, pos
