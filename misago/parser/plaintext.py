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
    result: str = ""

    def push(self, text: str, nlnl: bool = False):
        if nlnl and self.result:
            self.result += "\n\n"
        self.result += text


class RendererPlaintext(RendererProtocol):
    __output__ = "text"

    rules: list[RendererPlaintextRule]

    def __init__(self, rules: list[RendererPlaintextRule]):
        self.rules = rules

    def render(self, tokens: list[Token]) -> str:
        state = StatePlaintext(
            renderer=self,
            tokens=tokens,
            pos=0,
            posMax=len(tokens) - 1,
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
            render_attachments,
            render_paragraph,
            render_inline,
            render_mention,
            render_softbreak,
            render_text,
        ],
    )

    # table cell
    # list item
    # link
    # autolink
    # linkify
    # image
    # image bbcode
    # inline code


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

    state.push(state.renderer.render(tokens[1:-1]), nlnl=True)
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
        state.push(f"{info}, {syntax}:\n{content}", nlnl=True)
    elif info or syntax:
        state.push(f"{info or syntax}:\n{content}", nlnl=True)
    else:
        state.push(content, nlnl=True)

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

    state.push(prefix + state.renderer.render(tokens[1:-1]), nlnl=True)
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

    state.push(prefix + state.renderer.render(tokens[1:-1]), nlnl=True)
    state.pos = pos

    return True


def render_ordered_list(state: StatePlaintext) -> bool:
    match = match_token_pair(state, "ordered_list_open", "ordered_list_close")
    if not match:
        return False

    tokens, pos = match
    content = render_list_content(state, tokens)

    state.push(content, nlnl=True)
    state.pos = pos
    return True


def render_bullet_list(state: StatePlaintext) -> bool:
    match = match_token_pair(state, "bullet_list_open", "bullet_list_close")
    if not match:
        return False

    tokens, pos = match
    content = render_list_content(state, tokens)

    state.push(content, nlnl=True)
    state.pos = pos
    return True


def render_list_content(
    state: StatePlaintext, tokens: list[Token], prefix: str | None = None
) -> str:
    prefix = f"{prefix} " if prefix else ""

    opening_token = tokens[0]
    is_ordered = opening_token.type == "ordered_list_open"

    if is_ordered:
        start = opening_token.attrs.get("start") or 1
    else:
        delimiter = opening_token.markup

    nesting_item = 0
    nesting_list = 0

    list_items: list[list[Token]] = []
    list_item: list[Token] = []
    for token in tokens[1:-1]:
        if token.type in ("ordered_list_open", "bullet_list_open"):
            nesting_list += 1
        elif token.type in ("ordered_list_close", "bullet_list_close"):
            nesting_list -= 1
        elif token.type == "list_item_open":
            nesting_item += 1
        elif token.type == "list_item_close":
            nesting_item -= 1
            if not nesting_item and not nesting_list:
                list_items.append(list_item)
                list_item = []
        elif nesting_item:
            list_item.append(token)

    rendered_items: list[str] = []
    for index, item_tokens in enumerate(list_items):
        if is_ordered:
            item_prefix = f"{prefix}{start + index}. "
        else:
            item_prefix = f"{prefix} {delimiter} "

        item_str = item_prefix
        item_str += state.renderer.render(item_tokens).strip()

        rendered_items.append(item_str.strip())

    return "\n".join(rendered_items)


def render_attachments(state: StatePlaintext) -> bool:
    match = match_token_pair(state, "attachments_open", "attachments_close")
    if not match:
        return False

    tokens, pos = match
    attachments = tokens[1:-1]

    content: list[str] = []
    for attachment in attachments:
        if attachment.type == "attachment":
            if name := attachment.attrs.get("name"):
                content.append(name)

    if content:
        state.push("\n".join(content), nlnl=True)

    state.pos = pos

    return True


def render_paragraph(state: StatePlaintext) -> bool:
    match = match_token_pair(state, "paragraph_open", "paragraph_close")
    if not match:
        return False

    tokens, pos = match

    state.push(state.renderer.render(tokens[1:-1]), nlnl=True)
    state.pos = pos

    return True


# def render_attachment(
#     renderer: RendererPlaintext, tokens: list[Token], idx: int
# ) -> str:
#     name = tokens[idx].attrs["name"]
#     return f"\n{name}"


# def render_block(
#     renderer: RendererPlaintext, tokens: list[Token], idx: int
# ) -> str | None:
#     try:
#         next_token = tokens[idx + 1]
#     except IndexError:
#         return None

#     if next_token.type != "inline":
#         return None

#     content = renderer.render(tokens[idx + 1].children)

#     if idx:
#         return f"\n\n{content}"

#     return content


# def render_hard_break(
#     renderer: RendererPlaintext, tokens: list[Token], idx: int
# ) -> str | None:
#     if idx:
#         return "\n\n"

#     return None


# def render_code(
#     renderer: RendererPlaintext, tokens: list[Token], idx: int
# ) -> str | None:
#     token = tokens[idx]

#     info = token.attrs.get("info")
#     syntax = token.attrs.get("syntax")

#     prefix = "" if idx else "\n\n"
#     content = token.content

#     if info and syntax:
#         return f"{prefix}{info}, {syntax}:\n\n{content}"

#     if info or syntax:
#         return f"{prefix}{info or syntax}:\n\n{content}"

#     return f"{prefix}{content}"


# def render_quote_bbcode_open(
#     renderer: RendererPlaintext, tokens: list[Token], idx: int
# ) -> str | None:
#     info = tokens[idx].attrs.get("info")
#     user = tokens[idx].attrs.get("user")

#     if idx and (info or user):
#         return f"\n\n{info or user}:"
#     elif info or user:
#         return f"{info or user}:"

#     return None


# def render_spoiler_bbcode_open(
#     renderer: RendererPlaintext, tokens: list[Token], idx: int
# ) -> str | None:
#     info = tokens[idx].attrs.get("info")

#     if idx and info:
#         return f"\n\n{info}:"
#     elif info:
#         return f"{info}:"

#     return None


# def render_ordered_list(
#     renderer: RendererPlaintext, tokens: list[Token], idx: int
# ) -> str | None:
#     print(tokens[idx])
#     return None


def render_inline(state: StatePlaintext) -> bool:
    token = state.tokens[state.pos]
    if token.type != "inline":
        return False

    state.push(state.renderer.render(token.children))
    state.pos += 1
    return True


def render_mention(state: StatePlaintext) -> bool:
    token = state.tokens[state.pos]
    if token.type != "mention":
        return False

    state.push(token.markup)
    state.pos += 1
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
