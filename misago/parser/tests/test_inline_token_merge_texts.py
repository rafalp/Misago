from markdown_it.token import Token

from ..tokens import inline_token_merge_texts


def test_inline_token_merge_texts_merges_text_tokens_contents(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("Lorem")
    assert tokens[1].type == "inline"

    inline_token = tokens[1]
    inline_token.children.append(
        Token(type="text", tag="", content=" ipsum", nesting=0)
    )
    inline_token.children.append(
        Token(type="text", tag="", content=" dolor", nesting=0)
    )
    inline_token.children.append(Token(type="text", tag="", content=" met.", nesting=0))

    inline_token = inline_token_merge_texts(inline_token)
    assert len(inline_token.children) == 1
    assert inline_token.children[0].type == "text"
    assert inline_token.children[0].content == "Lorem ipsum dolor met."


def test_inline_token_merge_texts_merges_text_tokens_contents_around_other_tokens(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("Lorem")
    assert tokens[1].type == "inline"

    inline_token = tokens[1]
    inline_token.children.append(
        Token(type="text", tag="", content=" ipsum", nesting=0)
    )
    inline_token.children.append(Token(type="t_open", tag="t", nesting=1))
    inline_token.children.append(
        Token(type="text", tag="", content=" dolor", nesting=0)
    )
    inline_token.children.append(Token(type="t_close", tag="t", nesting=-1))
    inline_token.children.append(Token(type="text", tag="", content=" met", nesting=0))
    inline_token.children.append(
        Token(type="text", tag="", content=" elit.", nesting=0)
    )

    inline_token = inline_token_merge_texts(inline_token)
    assert len(inline_token.children) == 5
    assert inline_token.children[0].type == "text"
    assert inline_token.children[0].content == "Lorem ipsum"
    assert inline_token.children[-1].type == "text"
    assert inline_token.children[-1].content == " met elit."
