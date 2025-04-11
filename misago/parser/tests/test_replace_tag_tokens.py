from markdown_it.token import Token

from ..tokens import replace_tag_tokens


def test_replace_tag_tokens_replaces_element(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("Hello world")

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "paragraph_open"
        assert tokens[1].type == "inline"
        assert tokens[2].type == "paragraph_close"
        assert stack == []

        return [replacement]

    assert replace_tag_tokens(tokens, "p", replace_func) == [replacement]


def test_replace_tag_tokens_passes_stack_to_replace_func(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("> Hello world")

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "paragraph_open"
        assert tokens[1].type == "inline"
        assert tokens[2].type == "paragraph_close"

        assert len(stack) == 1
        assert stack[0].tag == "blockquote"

        return [replacement]

    assert replacement in replace_tag_tokens(tokens, "p", replace_func)


def test_replace_tag_tokens_replaces_void_element(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("- - -")

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "hr"
        assert stack == []

        return [replacement]

    assert replace_tag_tokens(tokens, "hr", replace_func) == [replacement]
