from ..tokens import tokens_contain_tag


def test_tokens_contain_tag_returns_true_if_tag_is_found(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("Hello world\n> quote\nLorem ipsum")
    assert tokens_contain_tag(tokens, "blockquote")


def test_tokens_contain_tag_returns_true_if_nested_tag_is_found(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("> quote")
    assert tokens_contain_tag(tokens, "p")


def test_tokens_contain_tag_returns_false_if_tag_is_not_found(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("Hello world\n\nLorem ipsum")
    assert not tokens_contain_tag(tokens, "blockquote")


def test_tokens_contain_tag_returns_true_if_void_tag_is_found(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("Hello world\n- - -\nLorem ipsum")
    assert tokens_contain_tag(tokens, "hr")


def test_tokens_contain_tag_returns_true_if_nested_void_tag_is_found(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("> - - -")
    assert tokens_contain_tag(tokens, "hr")


def test_tokens_contain_tag_returns_false_if_void_tag_is_not_found(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("Hello world\n\nLorem ipsum")
    assert not tokens_contain_tag(tokens, "hr")
