from dataclasses import replace
from typing import Callable

from markdown_it.token import Token


def replace_tag_tokens(
    tokens: list[Token],
    tag: str,
    replace_func: Callable[[list[Token], list[Token]], list[Token]],
) -> list[Token]:
    nesting: int = 0
    stack: list[Token] = []
    tag_tokens: list[Token] = []
    new_tokens: list[Token] = []

    for token in tokens:
        if token.tag == tag:
            if token.nesting == 0:
                new_tokens += replace_func([token], stack)
            else:
                nesting += token.nesting
                tag_tokens.append(token)

                if not nesting:
                    new_tokens += replace_func(tag_tokens, stack)
                    tag_tokens = []

        elif nesting:
            tag_tokens.append(token)

        else:
            new_tokens.append(token)
            if token.nesting == 1:
                stack.append(token)
            if token.nesting == -1:
                stack.pop()

    return new_tokens


def replace_inline_tag_tokens(
    tokens: list[Token],
    tag: str,
    replace_func: Callable[[list[Token], list[Token]], list[Token]],
) -> list[Token]:
    new_tokens: list[Token] = []

    for token in tokens:
        if token.type == "inline":
            new_tokens.append(
                replace(
                    token,
                    children=replace_tag_tokens(token.children, tag, replace_func),
                )
            )
        else:
            new_tokens.append(token)

    return new_tokens


def tokens_contain_tag(tokens: list[Token], tag: str) -> bool:
    nesting = 0
    for token in tokens:
        if token.tag == tag:
            nesting += token.nesting
            if nesting == 0:
                return True

    return False


def tokens_contain_inline_tag(tokens: list[Token], tag: str) -> bool:
    for token in tokens:
        if token.type == "inline" and tokens_contain_tag(token.children, tag):
            return True

    return False
