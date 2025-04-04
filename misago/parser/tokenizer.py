from dataclasses import replace
from typing import Callable

from markdown_it import MarkdownIt
from markdown_it.token import Token

from .hooks import tokenize_hook
from .mentions import replace_mentions_tokens
from .shortenurl import shorten_url

TokensProcessor = Callable[[list[Token]], list[Token] | None]


def tokenize(parser: MarkdownIt, markup: str) -> list[Token]:
    return tokenize_hook(
        _tokenize_action,
        parser,
        markup,
        [
            set_tables_styles,
            shorten_link_text,
            extract_attachments,
            remove_repeated_hrs,
            remove_nested_inline_bbcodes,
            replace_blockquotes_with_misago_quotes,
            replace_mentions_tokens,
            set_links_rel_external_nofollow_noopener,
            set_links_target_blank,
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


def set_links_rel_external_nofollow_noopener(tokens: list[Token]) -> None:
    for token in tokens:
        if token.type == "inline":
            for child in token.children:
                if child.tag == "a" and child.nesting == 1:
                    child.attrSet("rel", "external nofollow noopener")


def set_links_target_blank(tokens: list[Token]) -> None:
    for token in tokens:
        if token.type == "inline":
            for child in token.children:
                if child.tag == "a" and child.nesting == 1:
                    child.attrSet("target", "_blank")


def set_tables_styles(tokens: list[Token]) -> None:
    for token in tokens:
        if token.type == "table_open":
            token.attrSet("class", "rich-text-table")


def shorten_link_text(tokens: list[Token]) -> None:
    link_tokens: list[Token] = []

    for token in tokens:
        if token.children:
            shorten_link_text(token.children)

        if token.type in ("link_open", "link_close") or link_tokens:
            link_tokens.append(token)
            if token.type == "link_close":
                _shorten_link_text_token_content(link_tokens)
                link_tokens = []


def _shorten_link_text_token_content(tokens: list[Token]):
    if len(tokens) != 3:
        return

    link_open, text, _ = tokens
    href = link_open.attrs.get("href")

    if href and text.content == href:
        link_open.meta["shortened_url"] = True
        text.content = shorten_url(text.content)


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

    return merge_attachments_groups(new_tokens)


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

        elif clean_children := clean_inline_slice(children):
            new_tokens.append(p_open)
            new_tokens.append(
                Token(
                    type="inline",
                    tag="",
                    nesting=0,
                    level=inline.level,
                    children=clean_children,
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


def merge_attachments_groups(tokens: list[Token]) -> list[Token]:
    if not tokens:
        return tokens

    new_tokens: list[Token] = []
    max_index = len(tokens) - 1

    # Merge attachments groups basically removes </close><open> token pairs
    for index, token in enumerate(tokens):
        if (
            token.type == "attachments_open"
            and index
            and tokens[index - 1].type == "attachments_close"
        ):
            continue

        if (
            token.type == "attachments_close"
            and index < max_index
            and tokens[index + 1].type == "attachments_open"
        ):
            continue

        new_tokens.append(token)

    return new_tokens


def remove_repeated_hrs(tokens: list[Token]) -> list[Token]:
    if not tokens:
        return []

    new_tokens: list[Token] = []
    for token in tokens:
        if not new_tokens or token.tag != "hr" or new_tokens[-1].tag != "hr":
            new_tokens.append(token)

    return new_tokens


def remove_nested_inline_bbcodes(tokens: list[Token]) -> list[Token]:
    if not tokens:
        return []

    for token in tokens:
        if token.type == "inline":
            _remove_nested_inline_bbcodes_from_inline_token(token)

    return tokens


INLINE_BBCODE_OPEN_TAGS = (
    "bold_bbcode_open",
    "italics_bbcode_open",
    "underline_bbcode_open",
    "strikethrough_bbcode_open",
)

INLINE_BBCODE_CLOSE_TAGS = (
    "bold_bbcode_close",
    "italics_bbcode_close",
    "underline_bbcode_close",
    "strikethrough_bbcode_close",
)


def _remove_nested_inline_bbcodes_from_inline_token(token_inline: Token):
    new_children: list[Token] = []
    stack: list[str] = []

    for token in token_inline.children:
        if token.type in INLINE_BBCODE_OPEN_TAGS:
            if token.tag not in stack:
                new_children.append(token)
            stack.append(token.tag)

        elif token.type in INLINE_BBCODE_CLOSE_TAGS:
            if stack and stack[-1] == token.tag:
                stack.pop(-1)
            if token.tag not in stack:
                new_children.append(token)

        elif token.type == "text" and new_children and new_children[-1].type == "text":
            new_children[-1].content += token.content

        else:
            new_children.append(token)

    token_inline.children = new_children


def replace_blockquotes_with_misago_quotes(tokens: list[Token]) -> list[Token]:
    for token in tokens:
        if token.tag == "blockquote":
            token.tag = "misago-quote"

    return tokens


def clean_inline_slice(tokens: list[Token]) -> list[Token]:
    if not tokens:
        return []

    new_tokens: list[Token] = []

    # 1st pass: clear orphaned closing tags
    stack: list[tuple[int, str]] = []
    for index, token in enumerate(tokens):
        if token.nesting == 1:
            stack.append((index, token.type))
        if token.nesting == -1:
            if not stack or stack[-1][1] != token.type:
                new_tokens.append(
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

        new_tokens.append(token)

    # 2nd pass: replace orphaned opening tags
    for index, token in stack:
        new_tokens[index] = Token(
            type="text",
            tag="",
            nesting=0,
            content=new_tokens[index].markup,
        )

    # 3rd pass: merge text nodes
    new_tokens = merge_text_nodes(new_tokens)

    # 4rd pass: strip whitespace from beginning and end of slice
    return strip_inline_nodes(new_tokens)


def merge_text_nodes(tokens: list[Token]) -> list[Token]:
    new_tokens: list[Token] = []
    for token in tokens:
        if token.type == "text" and new_tokens and new_tokens[-1].type == "text":
            new_tokens[-1].content += token.content
        else:
            new_tokens.append(token)
    return new_tokens


def strip_inline_nodes(tokens: list[Token]) -> list[Token]:
    if not tokens:
        return tokens

    new_tokens: list[Token] = tokens[:]

    # lstrip
    while new_tokens and new_tokens[0].type in ("text", "softbreak"):
        if new_tokens[0].type == "text":
            new_tokens[0].content = new_tokens[0].content.lstrip()
            if not new_tokens[0].content:
                new_tokens = new_tokens[1:]
            else:
                break

        elif new_tokens[0].type == "softbreak":
            new_tokens = new_tokens[1:]

    # rstrip
    while new_tokens and new_tokens[-1].type in ("text", "softbreak"):
        if new_tokens[-1].type == "text":
            new_tokens[-1].content = new_tokens[-1].content.rstrip()
            if not new_tokens[-1].content:
                new_tokens = new_tokens[:-1]
            else:
                break

        elif new_tokens[-1].type == "softbreak":
            new_tokens = new_tokens[:-1]

    return new_tokens
