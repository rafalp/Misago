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
            render_paragraph,
            render_inline,
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


def render_paragraph(state: StatePlaintext) -> bool:
    match = match_token_pair(state, "paragraph_open", "paragraph_close")
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


# def render_mention(renderer: RendererPlaintext, tokens: list[Token], idx: int) -> str:
#     return tokens[idx].markup


def render_inline(state: StatePlaintext) -> bool:
    token = state.tokens[state.pos]
    if token.type != "inline":
        return False

    state.push(state.renderer.render(token.children))
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
