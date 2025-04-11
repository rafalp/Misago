from ..tokens import tokens_contain_inline_tag


def test_tokens_contain_inline_tag_returns_true_if_inline_tag_is_found(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("Lorem [b]ipsum[/b] dolor")
    assert tokens_contain_inline_tag(tokens, "b")


def test_tokens_contain_inline_tag_returns_true_if_nested_inline_tag_is_found(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("> Lorem [b]ipsum[/b] dolor")
    assert tokens_contain_inline_tag(tokens, "b")


def test_tokens_contain_inline_tag_returns_false_if_inline_tag_is_not_found(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("Lorem ipsum dolor")
    assert not tokens_contain_inline_tag(tokens, "b")
