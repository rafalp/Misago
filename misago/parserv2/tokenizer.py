from dataclasses import replace
from typing import Callable

from markdown_it import MarkdownIt
from markdown_it.token import Token

from .hooks import tokenize_hook


TokensProcessor = Callable[[list[Token]], list[Token] | None]


def tokenize(parser: MarkdownIt, markup: str) -> list[Token]:
    return tokenize_hook(
        _tokenize_action,
        parser,
        markup,
        [
            extract_attachments,
        ],
    )


def _tokenize_action(
    parser: MarkdownIt,
    markup: str,
    processors: list[TokensProcessor],
) -> list[Token]:
    tokens = parser.parse(markup)
    for processor in processors:
        tokens = processor(tokens) or tokens
    return tokens


def extract_attachments(tokens: list[Token]) -> list[Token] | None:
    nesting: int = 0
    paragraph: list[Token] = []
    new_tokens: list[Token] = []

    for token in tokens:
        if token.tag == "p":
            nesting += token.nesting
            paragraph.append(token)

            if not nesting:
                new_tokens += _extract_attachments_from_paragraph(paragraph)
                paragraph = []

        elif nesting:
            paragraph.append(token)

        else:
            new_tokens.append(token)

    if paragraph:
        new_tokens += _extract_attachments_from_paragraph(paragraph)

    return new_tokens


def _extract_attachments_from_paragraph(tokens: list[Token]) -> list[Token]:
    p_open, inline, p_close = tokens

    if not _inline_contains_attachments(inline):
        return tokens

    groups: list[tuple[bool, list[Token]]] = []
    for child in inline.children:
        if child.type == "attachment":
            if not groups or not groups[-1][0]:
                groups.append((True, []))
        else:
            if (
                groups
                and groups[-1][0]
                and child.type == "text"
                and not child.content.strip()
            ):
                continue

            if not groups or groups[-1][0]:
                groups.append((False, []))

        groups[-1][1].append(child)

    new_tokens: list[Token] = []
    for attachments, children in groups:
        if attachments:
            new_tokens.append(
                Token(
                    type="attachments_open",
                    tag="div",
                    nesting=1,
                    attrs={"class": "rich-text-attachment-group"},
                    block=True,
                ),
            )

            for attachment in children:
                new_tokens.append(replace(attachment, block=True))

            new_tokens.append(
                Token(
                    type="attachments_close",
                    tag="div",
                    nesting=-1,
                    block=True,
                ),
            )

        elif children:
            if children[0].type == "text":
                children[0].content = children[0].content.lstrip()
            if children[-1].type == "text":
                children[-1].content = children[-1].content.rstrip()

            new_tokens.append(p_open)
            new_tokens.append(
                Token(
                    type="inline",
                    tag="",
                    nesting=0,
                    level=inline.level,
                    children=children,
                    block=True,
                )
            )
            new_tokens.append(p_close)

    return new_tokens


def _inline_contains_attachments(token: Token) -> bool:
    for child in token.children:
        if child.type == "attachment":
            return True

    return False
