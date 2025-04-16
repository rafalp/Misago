from dataclasses import replace
from typing import Callable

from markdown_it import MarkdownIt
from markdown_it.token import Token

from .hooks import tokenize_hook
from .mentions import replace_mentions_tokens
from .shortenurl import shorten_url
from .tokens import (
    ReplaceTokensStrategy,
    replace_inline_tag_tokens,
    replace_tag_tokens,
    split_inline_token,
    tokens_contain_inline_tag,
    tokens_contain_tag,
)
from .youtube import parse_youtube_link

TokensProcessor = Callable[[list[Token]], list[Token] | None]


def tokenize(parser: MarkdownIt, markup: str) -> list[Token]:
    return tokenize_hook(
        _tokenize_action,
        parser,
        markup,
        [
            replace_video_links_with_players,
            shorten_link_text,
            extract_attachments,
            remove_repeated_hrs,
            remove_nested_inline_bbcodes,
            replace_blockquotes_with_misago_quotes,
            replace_mentions_tokens,
            set_links_rel_external_nofollow_noopener,
            set_links_target_blank,
            make_tables_responsive,
            set_tables_styles,
            set_lists_type_metadata,
            set_lists_styles,
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


LIST_OPEN_TYPES = ("bullet_list_open", "ordered_list_open")
LIST_TAGS = ("ol", "ul")


def set_lists_type_metadata(tokens: list[Token]) -> None:
    if not tokens_contain_tag(tokens, "li"):
        return tokens

    replace_tag_tokens(tokens, "ol", _set_list_type_metadata)
    replace_tag_tokens(tokens, "ul", _set_list_type_metadata)

    return tokens


def _set_list_type_metadata(tokens: list[Token], stack: list[Token]) -> list[Token]:
    list_open, items = tokens[0], tokens[1:-1]
    list_open.meta["tight"] = True

    replace_tag_tokens(items, list_open.tag, _set_list_type_metadata)
    replace_tag_tokens(tokens, "li", set_list_item_type_metadata)

    nesting = 0
    for child_token in items:
        if child_token.tag in LIST_TAGS:
            nesting += child_token.nesting

        if (
            not nesting
            and child_token.tag == "li"
            and child_token.meta.get("tight") is False
        ):
            list_open.meta["tight"] = False

    if not list_open.meta["tight"]:
        unhide_loose_list_paragraphs(items)

    return tokens


def unhide_loose_list_paragraphs(tokens: list[Token]):
    nesting = 0
    for token in tokens:
        if token.tag in LIST_TAGS:
            nesting += token.nesting

        if not nesting and token.tag == "p":
            token.hidden = False


def set_list_item_type_metadata(tokens: list[Token], stack: list[Token]) -> list[Token]:
    item_open, items = tokens[0], tokens[1:-1]
    item_open.meta["tight"] = True

    replace_tag_tokens(items, "li", set_list_item_type_metadata)

    nesting = 0
    for child_token in items:
        if child_token.tag == "li":
            nesting += child_token.nesting

        if not nesting and child_token.type != "inline" and not child_token.hidden:
            item_open.meta["tight"] = False

    return tokens


def set_lists_styles(tokens: list[Token]) -> None:
    for token in tokens:
        if token.type in LIST_OPEN_TYPES:
            if token.meta.get("tight") is False:
                class_name = "rich-text-list-loose"
            else:
                class_name = "rich-text-list-tight"

            token.attrSet("class", class_name)


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


def replace_video_links_with_players(tokens: list[Token]) -> list[Token] | None:
    if not tokens_contain_inline_tag(tokens, "a"):
        return tokens

    tokens = replace_tag_tokens(tokens, "p", replace_paragraph_videos)
    tokens = replace_tag_tokens(tokens, "td", replace_table_videos)
    return tokens


def replace_paragraph_videos(tokens: list[Token], stack: list[Token]) -> list[Token]:
    if "list_item_open" in [t.type for t in stack]:
        return tokens

    tokens_with_video = replace_inline_tag_tokens(
        tokens,
        "a",
        replace_inline_videos_links,
        ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE,
    )
    if not tokens_contain_inline_tag(tokens_with_video, "misago-video"):
        return tokens

    p_open, inline, p_close = tokens_with_video

    new_tokens: list[Token] = []
    for part in split_inline_token(inline, "misago-video"):
        if part.type == "video":
            new_tokens.append(part)
        else:
            new_tokens += [p_open, part, p_close]
    return new_tokens


def replace_table_videos(tokens: list[Token], stack: list[Token]) -> list[Token]:
    tokens_with_video = replace_inline_tag_tokens(
        tokens, "a", replace_inline_videos_links, ReplaceTokensStrategy.ONLY_CHILD
    )
    if not tokens_contain_inline_tag(tokens_with_video, "misago-video"):
        return tokens

    td_open, inline, td_close = tokens_with_video

    new_tokens: list[Token] = []
    for part in split_inline_token(inline, "misago-video"):
        new_tokens += [td_open, part, td_close]
    return new_tokens


def replace_inline_videos_links(tokens: list[Token], stack: list[Token]) -> list[Token]:
    link_open = tokens[0]
    if link_open.markup != "linkify":
        return tokens

    href = link_open.attrs.get("href")
    if not href:
        return tokens

    attrs = {"href": href}
    if youtube_video := parse_youtube_link(href):
        attrs["site"] = "youtube"
        attrs.update(youtube_video)
    else:
        return tokens

    return [
        Token(
            type="video",
            tag="misago-video",
            attrs=attrs,
            nesting=0,
            block=True,
        )
    ]


def make_tables_responsive(tokens: list[Token]) -> list[Token]:
    return replace_tag_tokens(tokens, "table", _make_table_responsive)


def _make_table_responsive(tokens: list[Token], stack: list[Token]) -> list[Token]:
    container_open = Token(
        type="table_container_open",
        tag="div",
        attrs={"class": "rich-text-table-container"},
        nesting=1,
        block=True,
    )

    container_close = Token(
        type="table_container_open",
        tag="div",
        nesting=-1,
        block=True,
    )

    return [container_open] + tokens + [container_close]


def extract_attachments(tokens: list[Token]) -> list[Token] | None:
    new_tokens = replace_tag_tokens(tokens, "p", _extract_attachments_from_paragraph)
    return merge_attachments_groups(new_tokens)


def _extract_attachments_from_paragraph(
    tokens: list[Token], stack: list[Token]
) -> list[Token]:
    if not tokens_contain_inline_tag(tokens, "misago-attachment"):
        return tokens

    p_open, inline, p_close = tokens

    attachments_open = Token(
        type="attachments_open",
        tag="div",
        nesting=1,
        attrs={"class": "rich-text-attachment-group"},
        block=True,
    )

    attachments_close = Token(
        type="attachments_close",
        tag="div",
        nesting=-1,
        block=True,
    )

    new_tokens: list[Token] = []
    for part in split_inline_token(inline, "misago-attachment"):
        if part.type == "attachment":
            if not new_tokens or new_tokens[-1].type != "attachment":
                new_tokens.append(attachments_open)
            new_tokens.append(replace(part, block=True))
        else:
            if new_tokens and new_tokens[-1].type == "attachment":
                new_tokens.append(attachments_close)
            new_tokens += [p_open, part, p_close]

    if new_tokens and new_tokens[-1].type == "attachment":
        new_tokens.append(attachments_close)

    p_open.hidden = False
    p_close.hidden = False

    return new_tokens


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


INLINE_BBCODE_OPEN_TYPES = (
    "bold_bbcode_open",
    "italics_bbcode_open",
    "underline_bbcode_open",
    "strikethrough_bbcode_open",
)

INLINE_BBCODE_CLOSE_TYPES = (
    "bold_bbcode_close",
    "italics_bbcode_close",
    "underline_bbcode_close",
    "strikethrough_bbcode_close",
)


def _remove_nested_inline_bbcodes_from_inline_token(token_inline: Token):
    new_children: list[Token] = []
    stack: list[str] = []

    for token in token_inline.children:
        if token.type in INLINE_BBCODE_OPEN_TYPES:
            if token.tag not in stack:
                new_children.append(token)
            stack.append(token.tag)

        elif token.type in INLINE_BBCODE_CLOSE_TYPES:
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
