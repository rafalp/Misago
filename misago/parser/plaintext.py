from dataclasses import dataclass
from textwrap import dedent
from typing import Callable

from markdown_it.renderer import RendererProtocol
from markdown_it.token import Token

from .hooks import render_tokens_to_plaintext_hook


RendererPlaintextRule = Callable[["StatePlaintext"], bool]


@dataclass
class StatePlaintext:
    renderer: "RendererPlaintext"
    tokens: list[Token]
    pos: int
    posMax: int
    list_item_prefix: str
    result: str = ""

    def push(self, text: str, hardbreak: bool = False):
        if hardbreak and self.result:
            self.result += "\n\n"
        self.result += text


class RendererPlaintext(RendererProtocol):
    __output__ = "text"

    rules: list[RendererPlaintextRule]

    def __init__(self, rules: list[RendererPlaintextRule]):
        self.rules = rules

    def render(self, tokens: list[Token], list_item_prefix: str | None = None) -> str:
        state = StatePlaintext(
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

        # Normalize whitespace and linebreaks
        result = state.result.strip()

        while "\n " in result:
            result = result.replace("\n ", "\n")

        while " \n" in result:
            result = result.replace(" \n", "\n")

        while "\n\n\n" in result:
            result = result.replace("\n\n\n", "\n\n")

        while "  " in result:
            result = result.replace("  ", " ")

        return result


def render_tokens_to_plaintext(tokens: list[Token]) -> str:
    return render_tokens_to_plaintext_hook(
        _render_tokens_to_plaintext_action,
        tokens,
        [
            render_header,
            render_code,
            render_quote_bbcode,
            render_spoiler_bbcode,
            render_ordered_list,
            render_bullet_list,
            render_table,
            render_attachment,
            render_paragraph,
            render_inline,
            render_code_inline,
            render_mention,
            render_link,
            render_image,
            render_video,
            render_softbreak,
            render_text,
        ],
    )


def _render_tokens_to_plaintext_action(
    tokens: list[Token],
    rules: list[tuple[str, RendererPlaintextRule]],
) -> str:
    renderer = RendererPlaintext(rules)
    return renderer.render(tokens)


def render_header(state: StatePlaintext) -> bool:
    match = match_token_pair(state, "heading_open", "heading_close")
    if not match:
        return False

    tokens, pos = match

    state.push(state.renderer.render(tokens[1:-1]), hardbreak=True)
    state.pos = pos

    return True


def render_code(state: StatePlaintext) -> bool:
    token = state.tokens[state.pos]
    if token.type not in ("code_block", "fence", "code_bbcode"):
        return False

    info = token.attrs.get("info")
    syntax = token.attrs.get("syntax")
    content = dedent(token.content).strip()

    if info and syntax:
        state.push(f"{info}, {syntax}:\n{content}", hardbreak=True)
    elif info or syntax:
        state.push(f"{info or syntax}:\n{content}", hardbreak=True)
    else:
        state.push(content, hardbreak=True)

    state.pos += 1
    return True


def render_quote_bbcode(state: StatePlaintext) -> bool:
    match = match_token_pair(state, "quote_bbcode_open", "quote_bbcode_close")
    if not match:
        return False

    tokens, pos = match
    opening_token = tokens[0]

    info = opening_token.attrs.get("info")
    user = opening_token.attrs.get("user")
    post = opening_token.attrs.get("post")

    if user and post:
        prefix = f"{user}, #{post}:\n"
    elif user:
        prefix = f"{user}, #{post}:\n"
    elif post:
        prefix = f"#{post}:\n"
    elif info:
        prefix = f"{info}:\n"
    else:
        prefix = ""

    state.push(prefix + state.renderer.render(tokens[1:-1]), hardbreak=True)
    state.pos = pos

    return True


def render_spoiler_bbcode(state: StatePlaintext) -> bool:
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


def render_ordered_list(state: StatePlaintext) -> bool:
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


def render_bullet_list(state: StatePlaintext) -> bool:
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
    state: StatePlaintext, tokens: list[Token], prefix: str | None = None
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


def render_table(state: StatePlaintext) -> bool:
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


def render_attachment(state: StatePlaintext) -> bool:
    token = state.tokens[state.pos]
    if token.type != "attachment":
        return False

    if name := token.attrs.get("name"):
        state.push(name, hardbreak=True)

    state.pos += 1
    return True


def render_paragraph(state: StatePlaintext) -> bool:
    match = match_token_pair(state, "paragraph_open", "paragraph_close")
    if not match:
        return False

    tokens, pos = match

    state.push(state.renderer.render(tokens[1:-1]), hardbreak=True)
    state.pos = pos

    return True


def render_inline(state: StatePlaintext) -> bool:
    token = state.tokens[state.pos]
    if token.type != "inline":
        return False

    state.push(state.renderer.render(token.children))
    state.pos += 1
    return True


def render_code_inline(state: StatePlaintext) -> bool:
    token = state.tokens[state.pos]
    if token.type != "code_inline":
        return False

    state.push(token.content)
    state.pos += 1
    return True


def render_link(state: StatePlaintext) -> bool:
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


def render_image(state: StatePlaintext) -> bool:
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


def render_video(state: StatePlaintext) -> bool:
    token = state.tokens[state.pos]
    if token.type != "video":
        return False

    state.push(token.attrs["href"])
    state.pos += 1
    return True


def render_mention(state: StatePlaintext) -> bool:
    match = match_token_pair(state, "link_open", "link_close")
    if not match:
        return False

    tokens, pos = match
    if not tokens[0].meta.get("mention"):
        return False

    state.push(state.renderer.render(tokens[1:-1]))
    state.pos = pos
    return True


def render_softbreak(state: StatePlaintext) -> bool:
    token = state.tokens[state.pos]
    if token.type != "softbreak":
        return False

    state.push("\n")
    state.pos += 1
    return True


def render_text(state: StatePlaintext) -> bool:
    token = state.tokens[state.pos]
    if token.type != "text":
        return False

    state.push(token.content)
    state.pos += 1
    return True


def match_token_pair(
    state: StatePlaintext, type_open: str, type_close: str
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
