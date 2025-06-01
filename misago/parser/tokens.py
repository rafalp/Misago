from dataclasses import replace
from enum import IntEnum
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


class ReplaceTokensStrategy(IntEnum):
    # All occurrences are replaced
    ALL = 0

    # Only child occurrence is replaced
    ONLY_CHILD = 1

    # Occurrences are replaced if no other tokens of type exist
    ONLY_OF_TYPE = 2

    # Only child occurrence in a line is replaced
    ONLY_CHILD_IN_LINE = 3

    # Occurrences are replaced if no other tokens of type exist in a line
    ONLY_OF_TYPE_IN_LINE = 4


def replace_tag_tokens(
    tokens: list[Token],
    tag: str,
    replace_func: Callable[[list[Token], list[Token]], list[Token]],
    strategy: ReplaceTokensStrategy = 0,
) -> list[Token]:
    if strategy == ReplaceTokensStrategy.ALL:
        return _replace_all_tag_tokens(tokens, tag, replace_func)

    if strategy == ReplaceTokensStrategy.ONLY_CHILD:
        return _replace_only_child_tag_tokens(tokens, tag, replace_func)

    if strategy == ReplaceTokensStrategy.ONLY_OF_TYPE:
        return _replace_only_of_type_tag_tokens(tokens, tag, replace_func)

    if strategy == ReplaceTokensStrategy.ONLY_CHILD_IN_LINE:
        return _replace_only_child_tag_in_line_tokens(tokens, tag, replace_func)

    if strategy == ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE:
        return _replace_only_of_type_tag_in_line_tokens(tokens, tag, replace_func)


def _replace_all_tag_tokens(
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


def _replace_only_child_tag_tokens(
    tokens: list[Token],
    tag: str,
    replace_func: Callable[[list[Token], list[Token]], list[Token]],
) -> list[Token]:
    nesting: int = 0
    occurrences: list[bool] = []

    for token in tokens:
        if token.type == "text" and not token.content.strip():
            continue

        elif token.type in ("softbreak", "hardbreak"):
            continue

        elif token.tag == tag:
            if token.nesting == 0:
                occurrences.append(True)
            else:
                nesting += token.nesting
                if not nesting:
                    occurrences.append(True)

        elif not nesting:
            occurrences.append(False)

    if occurrences == [True]:
        return _replace_all_tag_tokens(tokens, tag, replace_func)

    return tokens


def _replace_only_of_type_tag_tokens(
    tokens: list[Token],
    tag: str,
    replace_func: Callable[[list[Token], list[Token]], list[Token]],
) -> list[Token]:
    nesting: int = 0
    occurrences: list[bool] = []

    for token in tokens:
        if token.type == "text" and not token.content.strip():
            continue

        elif token.type in ("softbreak", "hardbreak"):
            continue

        elif token.tag == tag:
            if token.nesting == 0:
                occurrences.append(True)
            else:
                nesting += token.nesting
                if not nesting:
                    occurrences.append(True)

        elif not nesting:
            occurrences.append(False)

    if occurrences and False not in occurrences:
        return _replace_all_tag_tokens(tokens, tag, replace_func)

    return tokens


def _replace_only_child_tag_in_line_tokens(
    tokens: list[Token],
    tag: str,
    replace_func: Callable[[list[Token], list[Token]], list[Token]],
) -> list[Token]:
    nesting: int = 0
    lines_occurrences: list[list[bool]] = [[]]

    for token in tokens:
        if token.type == "text" and not token.content.strip():
            continue

        elif token.type in ("softbreak", "hardbreak"):
            lines_occurrences.append([])
            continue

        elif token.tag == tag:
            if token.nesting == 0:
                lines_occurrences[-1].append(True)
            else:
                nesting += token.nesting
                if not nesting:
                    lines_occurrences[-1].append(True)

        elif not nesting:
            lines_occurrences[-1].append(False)

    nesting: int = 0
    line_no: int = 0
    stack: list[Token] = []
    tag_tokens: list[Token] = []
    new_tokens: list[Token] = []

    for token in tokens:
        if token.tag == tag:
            if lines_occurrences[line_no] == [True]:
                if token.nesting == 0:
                    new_tokens += replace_func([token], stack)
                else:
                    nesting += token.nesting
                    tag_tokens.append(token)

                    if not nesting:
                        new_tokens += replace_func(tag_tokens, stack)
                        tag_tokens = []
            else:
                if token.nesting == 0:
                    new_tokens.append(token)
                else:
                    nesting += token.nesting
                    tag_tokens.append(token)

                    new_tokens += tag_tokens
                    tag_tokens = []

        elif nesting:
            tag_tokens.append(token)

        else:
            if token.type in ("softbreak", "hardbreak"):
                line_no += 1

            new_tokens.append(token)
            if token.nesting == 1:
                stack.append(token)
            if token.nesting == -1:
                stack.pop()

    return new_tokens


def _replace_only_of_type_tag_in_line_tokens(
    tokens: list[Token],
    tag: str,
    replace_func: Callable[[list[Token], list[Token]], list[Token]],
) -> list[Token]:
    nesting: int = 0
    lines_occurrences: list[list[bool]] = [[]]

    for token in tokens:
        if token.type == "text" and not token.content.strip():
            continue

        elif token.tag == tag:
            if token.nesting == 0:
                lines_occurrences[-1].append(True)
            else:
                nesting += token.nesting
                if not nesting:
                    lines_occurrences[-1].append(True)

        elif not nesting:
            if token.type in ("softbreak", "hardbreak"):
                lines_occurrences.append([])
            else:
                lines_occurrences[-1].append(False)

    nesting: int = 0
    line_no: int = 0
    stack: list[Token] = []
    tag_tokens: list[Token] = []
    new_tokens: list[Token] = []

    for token in tokens:
        if token.tag == tag:
            if False not in lines_occurrences[line_no]:
                if token.nesting == 0:
                    new_tokens += replace_func([token], stack)
                else:
                    nesting += token.nesting
                    tag_tokens.append(token)

                    if not nesting:
                        new_tokens += replace_func(tag_tokens, stack)
                        tag_tokens = []
            else:
                if token.nesting == 0:
                    new_tokens.append(token)
                else:
                    nesting += token.nesting
                    tag_tokens.append(token)

                    new_tokens += tag_tokens
                    tag_tokens = []

        elif nesting:
            tag_tokens.append(token)

        else:
            if token.type in ("softbreak", "hardbreak"):
                line_no += 1

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
    strategy: ReplaceTokensStrategy = 0,
) -> list[Token]:
    new_tokens: list[Token] = []

    for token in tokens:
        if token.type == "inline":
            new_tokens.append(
                replace(
                    token,
                    children=replace_tag_tokens(
                        token.children, tag, replace_func, strategy
                    ),
                )
            )
        else:
            new_tokens.append(token)

    return new_tokens


def split_inline_token(token: Token, tag: str) -> list[Token]:
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
                clean_new_tokens.append(new_token)
        else:
            clean_new_tokens.append(new_token)

    return clean_new_tokens


def inline_token_remove_orphaned_children(token: Token) -> Token | None:
    new_children: list[Token] = []

    # 1st pass: replace orphaned closing tags
    stack: list[tuple[int, str]] = []
    for index, child in enumerate(token.children):
        if child.nesting == 1:
            stack.append((index, child.tag))
        if child.nesting == -1:
            if not stack or stack[-1][1] != child.tag:
                new_children.append(
                    Token(
                        type="text",
                        tag="",
                        nesting=0,
                        content=child.markup,
                    )
                )
                continue
            else:
                stack.pop()

        new_children.append(child)

    # 2nd pass: replace orphaned opening tags
    for index, _ in stack:
        new_children[index] = Token(
            type="text",
            tag="",
            nesting=0,
            content=new_children[index].markup,
        )

    if new_children:
        return inline_token_merge_texts(replace(token, children=new_children))

    return None


STRIP_TOKENS = ("text", "softbreak", "hardbreak")


def inline_token_strip(token: Token) -> Token | None:
    new_children: list[Token] = token.children[:]

    # lstrip
    while new_children and new_children[0].type in STRIP_TOKENS:
        if new_children[0].type == "text":
            new_children[0].content = new_children[0].content.lstrip()
            if not new_children[0].content:
                new_children = new_children[1:]
            else:
                break

        else:
            new_children = new_children[1:]

    # rstrip
    while new_children and new_children[-1].type in STRIP_TOKENS:
        if new_children[-1].type == "text":
            new_children[-1].content = new_children[-1].content.rstrip()
            if not new_children[-1].content:
                new_children = new_children[:-1]
            else:
                break

        else:
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
