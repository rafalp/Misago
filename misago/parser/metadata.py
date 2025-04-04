from markdown_it.token import Token

from .hooks import get_tokens_metadata_hook


def get_tokens_metadata(tokens: list[Token]) -> dict:
    return get_tokens_metadata_hook(_get_tokens_metadata_action, tokens)


def _get_tokens_metadata_action(tokens: list[Token]) -> dict:
    metadata = {}

    if attachments := get_attachments_metadata(tokens):
        metadata["attachments"] = attachments

    if get_highlight_code_metadata(tokens):
        metadata["highlight_code"] = True

    if posts := get_quoted_posts_metadata(tokens):
        metadata["posts"] = posts

    if mentions := get_mentions_metadata(tokens):
        metadata["mentions"] = mentions

    return metadata


def get_attachments_metadata(tokens: list[Token]) -> list[int]:
    attachments: set[int] = set()
    get_metadata_recursive(tokens, "attachment", "attachment", attachments)
    return sorted(attachments)


def get_highlight_code_metadata(tokens: list[Token]) -> list[str]:
    syntax: set[str] = set()
    get_metadata_recursive(tokens, "fence", "syntax", syntax)
    get_metadata_recursive(tokens, "code_bbcode", "syntax", syntax)
    return sorted(syntax)


def get_quoted_posts_metadata(tokens: list[Token]) -> list[int]:
    posts: set[int] = set()
    get_metadata_recursive(tokens, "quote_bbcode_open", "post", posts)
    return sorted(posts)


def get_mentions_metadata(tokens: list[Token]) -> list[int]:
    mentions: set[int] = set()
    get_metadata_recursive(tokens, "link_open", "mention", mentions)
    return sorted(mentions)


def get_metadata_recursive(
    tokens: list[Token], token_type: str, meta: str, data: set
) -> set:
    for token in tokens:
        if token.type == token_type and token.meta and token.meta.get(meta):
            data.add(token.meta[meta])

        if token.children:
            get_metadata_recursive(token.children, token_type, meta, data)
