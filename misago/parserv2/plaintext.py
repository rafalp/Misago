from typing import Callable

from markdown_it.renderer import RendererProtocol
from markdown_it.token import Token


class RendererPlaintext(RendererProtocol):
    __output__ = "text"

    rules: dict[str, Callable[[list[Token], int], str | None]]

    def __init__(self):
        self.rules = {}

    def add_rule(self, name: str, rule: Callable[[list[Token], int], str | None]):
        self.rules[name] = rule

    def render(self, tokens: list[Token]) -> str:
        result: str = ""
        for idx, token in enumerate(tokens):
            if rule := self.rules.get(token.type):
                token_result = rule(self, tokens, idx)
                if token_result is not None:
                    result += token_result

        while "\n\n\n" in result:
            result = result.replace("\n\n\n", "\n\n")

        while "  " in result:
            result = result.replace("  ", " ")

        return result.strip()


def render_plaintext(tokens: list[Token]) -> str:
    renderer = RendererPlaintext()

    renderer.add_rule("heading_open", render_block_open)
    renderer.add_rule("blockquote_open", render_block_open)
    renderer.add_rule("quote_bbcode_open", render_quote_bbcode_open)
    renderer.add_rule("spoiler_bbcode_open", render_spoiler_bbcode_open)
    renderer.add_rule("paragraph_open", render_block_open)

    renderer.add_rule("inline", render_inline)
    renderer.add_rule("softbreak", render_softbreak)
    renderer.add_rule("text", render_text)

    # code
    # fence
    # code bbcode
    # list item
    # table cell
    # link
    # autolink
    # linkify
    # image
    # image bbcode
    renderer.add_rule("text", render_text)

    return renderer.render(tokens)


def render_block_open(
    renderer: RendererPlaintext, tokens: list[Token], idx: int
) -> str | None:
    if idx:
        return "\n\n"

    return None


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


def render_text(renderer: RendererPlaintext, tokens: list[Token], idx: int) -> str:
    return tokens[idx].content
