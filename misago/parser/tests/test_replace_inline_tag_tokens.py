from markdown_it.token import Token

from ..tokens import replace_inline_tag_tokens


def test_replace_inline_tag_tokens_replaces_inline_element(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("Lorem [b]ipsum[/b] dolor")

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert tokens[1].type == "text"
        assert tokens[2].type == "bold_bbcode_close"
        assert stack == []

        return [replacement]

    updated_tokens = replace_inline_tag_tokens(tokens, "b", replace_func)
    assert len(updated_tokens) == 3
    assert updated_tokens[0].type == "paragraph_open"
    assert updated_tokens[1].type == "inline"
    assert updated_tokens[2].type == "paragraph_close"

    inline_tokens = updated_tokens[1].children
    assert len(inline_tokens) == 3
    assert inline_tokens[0].type == "text"
    assert inline_tokens[1] == replacement
    assert inline_tokens[2].type == "text"
