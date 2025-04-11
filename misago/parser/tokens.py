from dataclasses import replace
from typing import Callable

from markdown_it.token import Token


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


def inline_token_split(token: Token, tag: str) -> list[Token]:
    new_tokens: list[Token] = []
    new_children: list[Token] = []

    for child in token.children:
        if child.tag == tag:
            if new_children:
                new_tokens.append(replace(token, children=new_children))
                new_children = []

            new_tokens.append(child)
        else:
            new_children.append(child)

    if new_children:
        new_tokens.append(replace(token, children=new_children))

    clean_new_tokens = []
    for new_token in new_tokens:
        if new_token.type == "inline":
            new_token = inline_token_remove_orphaned_children(new_token)
            if new_token:
                new_token = inline_token_strip(new_token)
            if new_token:
                new_token = inline_token_merge_texts(new_token)
            if new_token:
                clean_new_tokens.append(clean_new_tokens)
        else:
            clean_new_tokens.append(new_token)

    return new_tokens


def inline_token_remove_orphaned_children(token: Token) -> Token | None:
    new_children: list[Token] = []

    # 1st pass: replace orphaned closing tags
    stack: list[tuple[int, str]] = []
    for index, token in enumerate(token.children):
        if token.nesting == 1:
            stack.append((index, token.type))
        if token.nesting == -1:
            if not stack or stack[-1][1] != token.type:
                new_children.append(
                    Token(
                        type="text",
                        tag="",
                        nesting=0,
                        content=token.markup,
                    )
                )
                continue
            else:
                stack.pop()

        new_children.append(token)

    # 2nd pass: replace orphaned opening tags
    for index, token in stack:
        new_children[index] = Token(
            type="text",
            tag="",
            nesting=0,
            content=new_children[index].markup,
        )

    if new_children:
        return replace(token, children=new_children)

    return None


def inline_token_strip(token: Token) -> Token | None:
    new_children: list[Token] = token.children[:]

    # lstrip
    while new_children and new_children[0].type in ("text", "softbreak"):
        if new_children[0].type == "text":
            new_children[0].content = new_children[0].content.lstrip()
            if not new_children[0].content:
                new_children = new_children[1:]
            else:
                break

        elif new_children[0].type == "softbreak":
            new_children = new_children[1:]

    # rstrip
    while new_children and new_children[-1].type in ("text", "softbreak"):
        if new_children[-1].type == "text":
            new_children[-1].content = new_children[-1].content.rstrip()
            if not new_children[-1].content:
                new_children = new_children[:-1]
            else:
                break

        elif new_children[-1].type == "softbreak":
            new_children = new_children[:-1]

    if new_children:
        return replace(token, children=new_children)

    return None


def inline_token_merge_texts(token: Token) -> Token | None:
    new_children: list[Token] = []
    for child in token.children:
        if child.type == "text" and new_children and new_children[-1].type == "text":
            new_children[-1].content += child.content
        else:
            new_children.append(child)
    return replace(token, children=new_children)
