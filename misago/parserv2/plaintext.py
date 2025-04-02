from typing import Callable

from markdown_it.renderer import RendererProtocol
from markdown_it.token import Token


RendererPlaintextRule = Callable[[list[Token], int], str | None]


class RendererPlaintext(RendererProtocol):
    __output__ = "text"

    rules: dict[str, RendererPlaintextRule]

    def __init__(self):
        self.rules = {}

    def add_rule(self, name: str, rule: RendererPlaintextRule):
        self.rules[name] = rule

    def render(self, tokens: list[Token]) -> str:
        result: str = ""
        for idx, token in enumerate(tokens):
            if rule := self.rules.get(token.type):
                token_result = rule(self, tokens, idx)
                if token_result is not None:
                    result += token_result

        # Normalize whitespace and linebreaks
        while "\n " in result:
            result = result.replace("\n ", "\n")

        while " \n" in result:
            result = result.replace(" \n", "\n")

        while "\n\n\n" in result:
            result = result.replace("\n\n\n", "\n\n")

        while "  " in result:
            result = result.replace("  ", " ")

        return result.strip()


def render_plaintext(tokens: list[Token]) -> str:
    return _render_plaintext_action(
        tokens,
        [
            ("attachments_open", render_softbreak),
            ("attachment", render_attachment),
            ("heading_open", render_block_open),
            ("blockquote_open", render_block_open),
            ("code_block", render_code),
            ("fence", render_code),
            ("code_bbcode", render_code),
            ("quote_bbcode_open", render_quote_bbcode_open),
            ("spoiler_bbcode_open", render_spoiler_bbcode_open),
            ("paragraph_open", render_block_open),
            ("inline", render_inline),
            ("softbreak", render_softbreak),
            ("mention", render_mention),
            ("text", render_text),
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


def _render_plaintext_action(
    tokens: list[Token],
    rules: list[tuple[str, RendererPlaintextRule]],
) -> str:
    renderer = RendererPlaintext()
    for name, rule in rules:
        renderer.add_rule(name, rule)

    return renderer.render(tokens)


def render_attachment(
    renderer: RendererPlaintext, tokens: list[Token], idx: int
) -> str:
    name = tokens[idx].attrs["name"]
    return f"\n{name}"


def render_block_open(
    renderer: RendererPlaintext, tokens: list[Token], idx: int
) -> str | None:
    if idx:
        return "\n\n"

    return None


def render_code(
    renderer: RendererPlaintext, tokens: list[Token], idx: int
) -> str | None:
    token = tokens[idx]

    info = token.attrs.get("info")
    syntax = token.attrs.get("syntax")

    prefix = "" if idx else "\n\n"
    content = token.content

    if info and syntax:
        return f"{prefix}{info}, {syntax}:\n\n{content}"

    if info or syntax:
        return f"{prefix}{info or syntax}:\n\n{content}"

    return f"{prefix}{content}"


def render_quote_bbcode_open(
    renderer: RendererPlaintext, tokens: list[Token], idx: int
) -> str | None:
    info = tokens[idx].attrs.get("info")
    user = tokens[idx].attrs.get("user")

    if idx and (info or user):
        return f"\n\n{info or user}:"
    elif info or user:
        return f"{info or user}:"

    return None


def render_spoiler_bbcode_open(
    renderer: RendererPlaintext, tokens: list[Token], idx: int
) -> str | None:
    info = tokens[idx].attrs.get("info")

    if idx and info:
        return f"\n\n{info}:"
    elif info:
        return f"{info}:"

    return None


def render_inline(renderer: RendererPlaintext, tokens: list[Token], idx: int) -> str:
    return renderer.render(tokens[idx].children)


def render_softbreak(
    renderer: RendererPlaintext, tokens: list[Token], idx: int
) -> str | None:
    if idx:
        return "\n"

    return None


def render_mention(renderer: RendererPlaintext, tokens: list[Token], idx: int) -> str:
    return tokens[idx].markup


def render_text(renderer: RendererPlaintext, tokens: list[Token], idx: int) -> str:
    return tokens[idx].content
