from unittest.mock import Mock

from markdown_it.token import Token

from ..tokens import ReplaceTokensStrategy, replace_tag_tokens


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


def test_replace_tag_tokens_only_child_strategy_replaces_only_child(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("[b]text[/b]")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_CHILD
    )
    assert result == [replacement]


def test_replace_tag_tokens_only_child_strategy_replaces_child_surrounded_by_spaces(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("t [b]text[/b] t")[1].children

    assert len(tokens) == 5
    tokens[0].content = "   "
    tokens[4].content = "   "

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_CHILD
    )
    assert result == [tokens[0], replacement, tokens[4]]


def test_replace_tag_tokens_only_child_strategy_doesnt_replace_child_surrounded_by_other_tokens(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("t [b]text[/b] t")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_CHILD
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_child_strategy_doesnt_replace_multiple_children(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("[b]text1[/b] [b]text2[/b]")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_CHILD
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_child_strategy_replaces_only_void_child(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("@bob")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_CHILD,
    )
    assert result == [replacement]


def test_replace_tag_tokens_only_child_strategy_replaces_void_child_surrounded_by_spaces(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("t @bob t")[1].children

    assert len(tokens) == 3
    tokens[0].content = "   "
    tokens[2].content = "   "

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_CHILD,
    )
    assert result == [tokens[0], replacement, tokens[2]]


def test_replace_tag_tokens_only_child_strategy_doesnt_replace_void_child_surrounded_by_other_tokens(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("hello @bob!")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_CHILD,
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_child_strategy_doesnt_replace_multiple_void_children(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("@bob @john")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_CHILD,
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_of_type_strategy_replaces_only_child(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("[b]text[/b]")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_OF_TYPE
    )
    assert result == [replacement]


def test_replace_tag_tokens_only_of_type_strategy_replaces_child_surrounded_by_spaces(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("t [b]text[/b] t")[1].children

    assert len(tokens) == 5
    tokens[0].content = "   "
    tokens[4].content = "   "

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_OF_TYPE
    )
    assert result == [tokens[0], replacement, tokens[4]]


def test_replace_tag_tokens_only_of_type_strategy_doesnt_replace_child_surrounded_by_other_tokens(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("t [b]text[/b] t")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_OF_TYPE
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_of_type_strategy_replaces_multiple_children_of_same_type(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("[b]text1[/b] [b]text2[/b]")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_OF_TYPE
    )
    assert result == [replacement, tokens[3], replacement]


def test_replace_tag_tokens_only_of_type_strategy_replaces_only_void_child(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("@bob")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_OF_TYPE,
    )
    assert result == [replacement]


def test_replace_tag_tokens_only_of_type_strategy_replaces_void_child_surrounded_by_spaces(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("t @bob t")[1].children

    assert len(tokens) == 3
    tokens[0].content = "   "
    tokens[2].content = "   "

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_OF_TYPE,
    )
    assert result == [tokens[0], replacement, tokens[2]]


def test_replace_tag_tokens_only_of_type_strategy_doesnt_replace_void_child_surrounded_by_other_tokens(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("hello @bob!")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_OF_TYPE,
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_of_type_strategy_replaces_multiple_void_children_of_same_type(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("@bob @john")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_OF_TYPE,
    )
    assert result == [replacement, tokens[1], replacement]


def test_replace_tag_tokens_only_child_in_line_strategy_replaces_only_child(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("[b]text[/b]")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE
    )
    assert result == [replacement]


def test_replace_tag_tokens_only_child_in_line_strategy_replaces_child_surrounded_by_spaces(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("t [b]text[/b] t")[1].children

    assert len(tokens) == 5
    tokens[0].content = "   "
    tokens[4].content = "   "

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE
    )
    assert result == [tokens[0], replacement, tokens[4]]


def test_replace_tag_tokens_only_child_in_line_strategy_doesnt_replace_child_surrounded_by_other_tokens(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("t [b]text[/b] t")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_child_in_line_strategy_doesnt_replace_multiple_children(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("[b]text1[/b] [b]text2[/b]")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_child_in_line_strategy_replaces_only_child_in_first_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("[b]text[/b]\nsecond line")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE
    )
    assert result == [replacement] + tokens[3:]


def test_replace_tag_tokens_only_child_in_line_strategy_replaces_only_child_in_middle_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n[b]text[/b]\nsecond line")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE
    )
    assert result == tokens[:2] + [replacement] + tokens[5:]


def test_replace_tag_tokens_only_child_in_line_strategy_replaces_only_child_in_last_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n[b]text[/b]")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE
    )
    assert result == tokens[:2] + [replacement]


def test_replace_tag_tokens_only_child_in_line_strategy_replaces_only_child_surrounded_by_spaces_in_first_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("[b]text[/b]    \nsecond line")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE
    )
    assert result == [replacement] + tokens[3:]


def test_replace_tag_tokens_only_child_in_line_strategy_replaces_only_child_surrounded_by_spaces_in_middle_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n   [b]text[/b]   \nsecond line")[
        1
    ].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE
    )
    assert result == tokens[:2] + [replacement] + tokens[5:]


def test_replace_tag_tokens_only_child_in_line_strategy_replaces_only_child_surrounded_by_spaces_in_last_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n   [b]text[/b]")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE
    )
    assert result == tokens[:2] + [replacement]


def test_replace_tag_tokens_only_child_in_line_strategy_doesnt_replace_only_child_surrounded_by_text_in_first_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("[b]text[/b]  text  \nsecond line")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_child_in_line_strategy_doesnt_replace_only_child_surrounded_by_text_in_middle_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n text  [b]text[/b]  text \nsecond line")[
        1
    ].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_child_in_line_strategy_doesnt_replace_only_child_surrounded_by_text_in_last_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n text  [b]text[/b]")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_child_in_line_strategy_doesnt_replace_multiple_children_in_first_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("[b]text[/b] [b]text2[/b]\nsecond line")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_child_in_line_strategy_doesnt_replace_multiple_children_in_middle_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n[b]text[/b] [b]text2[/b]\nsecond line")[
        1
    ].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_child_in_line_strategy_doesnt_replace_mutiple_children_in_last_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n[b]text[/b] [b]text2[/b]")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_child_in_line_strategy_replaces_only_void_child(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("@bob")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE,
    )
    assert result == [replacement]


def test_replace_tag_tokens_only_child_in_line_strategy_replaces_void_child_surrounded_by_spaces(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("t @bob t")[1].children

    assert len(tokens) == 3
    tokens[0].content = "   "
    tokens[2].content = "   "

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE,
    )
    assert result == [tokens[0], replacement, tokens[2]]


def test_replace_tag_tokens_only_child_in_line_strategy_doesnt_replace_void_child_surrounded_by_other_tokens(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("hello @bob!")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE,
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_child_in_line_strategy_doesnt_replace_multiple_void_children(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("@bob @john")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE,
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_child_in_line_strategy_replaces_only_void_child_in_first_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("@bob\nsecond line")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE,
    )
    assert result == [replacement] + tokens[1:]


def test_replace_tag_tokens_only_child_in_line_strategy_replaces_only_void_child_in_middle_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n@bob\nsecond line")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE,
    )
    assert result == tokens[:2] + [replacement] + tokens[3:]


def test_replace_tag_tokens_only_child_in_line_strategy_replaces_void_only_child_in_last_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n@bob")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE,
    )
    assert result == tokens[:2] + [replacement]


def test_replace_tag_tokens_only_child_in_line_strategy_replaces_only_void_child_surrounded_by_spaces_in_first_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("@bob    \nsecond line")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE,
    )
    assert result == [replacement] + tokens[1:]


def test_replace_tag_tokens_only_child_in_line_strategy_replaces_only_void_child_surrounded_by_spaces_in_middle_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n   @bob   \nsecond line")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE,
    )
    assert result == tokens[:2] + [replacement] + tokens[3:]


def test_replace_tag_tokens_only_child_in_line_strategy_replaces_only_void_child_surrounded_by_spaces_in_last_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n   @bob")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE,
    )
    assert result == tokens[:2] + [replacement]


def test_replace_tag_tokens_only_child_in_line_strategy_doesnt_replace_only_void_child_surrounded_by_text_in_first_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("@bob  text  \nsecond line")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE,
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_child_in_line_strategy_doesnt_replace_only_void_child_surrounded_by_text_in_middle_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n text  @bob  text \nsecond line")[
        1
    ].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE,
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_child_in_line_strategy_doesnt_replace_only_void_child_surrounded_by_text_in_last_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n text  @bob]")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE,
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_child_in_line_strategy_doesnt_replace_multiple_void_children_in_first_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("@bob @john\nsecond line")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE,
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_child_in_line_strategy_doesnt_replace_multiple_void_children_in_middle_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n@bob @john\nsecond line")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE,
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_child_in_line_strategy_doesnt_replace_mutiple_void_children_in_last_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n@bob @john")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_CHILD_IN_LINE,
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_only_child(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("[b]text[/b]")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE
    )
    assert result == [replacement]


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_child_surrounded_by_spaces(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("t [b]text[/b] t")[1].children

    assert len(tokens) == 5
    tokens[0].content = "   "
    tokens[4].content = "   "

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE
    )
    assert result == [tokens[0], replacement, tokens[4]]


def test_replace_tag_tokens_only_of_type_in_line_strategy_doesnt_replace_child_surrounded_by_other_tokens(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("t [b]text[/b] t")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_of_type_in_line_strategy_doesnt_replace_multiple_children(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("[b]text1[/b] [b]text2[/b]")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE
    )
    assert result == [replacement, tokens[3], replacement]


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_only_of_type_in_first_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("[b]text[/b]\nsecond line")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE
    )
    assert result == [replacement] + tokens[3:]


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_only_of_type_in_middle_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n[b]text[/b]\nsecond line")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE
    )
    assert result == tokens[:2] + [replacement] + tokens[5:]


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_only_of_type_in_last_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n[b]text[/b]")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE
    )
    assert result == tokens[:2] + [replacement]


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_only_of_type_surrounded_by_spaces_in_first_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("[b]text[/b]    \nsecond line")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE
    )
    assert result == [replacement] + tokens[3:]


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_only_of_type_surrounded_by_spaces_in_middle_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n   [b]text[/b]   \nsecond line")[
        1
    ].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE
    )
    assert result == tokens[:2] + [replacement] + tokens[5:]


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_only_of_type_surrounded_by_spaces_in_last_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n   [b]text[/b]")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE
    )
    assert result == tokens[:2] + [replacement]


def test_replace_tag_tokens_only_of_type_in_line_strategy_doesnt_replace_only_of_type_surrounded_by_text_in_first_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("[b]text[/b]  text  \nsecond line")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_of_type_in_line_strategy_doesnt_replace_only_of_type_surrounded_by_text_in_middle_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n text  [b]text[/b]  text \nsecond line")[
        1
    ].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_of_type_in_line_strategy_doesnt_replace_only_of_type_surrounded_by_text_in_last_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n text  [b]text[/b]")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_multiple_children_in_first_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("[b]text[/b] [b]text2[/b]\nsecond line")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE
    )
    assert result == [replacement, tokens[3], replacement] + tokens[7:]


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_multiple_children_in_middle_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n[b]text[/b] [b]text2[/b]\nsecond line")[
        1
    ].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE
    )
    assert result == tokens[:2] + [replacement, tokens[5], replacement] + tokens[9:]


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_mutiple_children_in_last_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n[b]text[/b] [b]text2[/b]")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 3
        assert tokens[0].type == "bold_bbcode_open"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens, "b", replace_func, strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE
    )
    assert result == tokens[:2] + [replacement, tokens[5], replacement]


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_only_void_child(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("@bob")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE,
    )
    assert result == [replacement]


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_void_child_surrounded_by_spaces(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("t @bob t")[1].children

    assert len(tokens) == 3
    tokens[0].content = "   "
    tokens[2].content = "   "

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE,
    )
    assert result == [tokens[0], replacement, tokens[2]]


def test_replace_tag_tokens_only_of_type_in_line_strategy_doesnt_replace_void_child_surrounded_by_other_tokens(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("hello @bob!")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE,
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_multiple_void_children(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("@bob @john")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE,
    )
    assert result == [replacement, tokens[1], replacement]


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_only_void_child_in_first_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("@bob\nsecond line")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE,
    )
    assert result == [replacement] + tokens[1:]


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_only_void_child_in_middle_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n@bob\nsecond line")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE,
    )
    assert result == tokens[:2] + [replacement] + tokens[3:]


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_void_only_of_type_in_last_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n@bob")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE,
    )
    assert result == tokens[:2] + [replacement]


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_only_void_child_surrounded_by_spaces_in_first_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("@bob    \nsecond line")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE,
    )
    assert result == [replacement] + tokens[1:]


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_only_void_child_surrounded_by_spaces_in_middle_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n   @bob   \nsecond line")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE,
    )
    assert result == tokens[:2] + [replacement] + tokens[3:]


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_only_void_child_surrounded_by_spaces_in_last_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n   @bob")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE,
    )
    assert result == tokens[:2] + [replacement]


def test_replace_tag_tokens_only_of_type_in_line_strategy_doesnt_replace_only_void_child_surrounded_by_text_in_first_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("@bob  text  \nsecond line")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE,
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_of_type_in_line_strategy_doesnt_replace_only_void_child_surrounded_by_text_in_middle_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n text  @bob  text \nsecond line")[
        1
    ].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE,
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_of_type_in_line_strategy_doesnt_replace_only_void_child_surrounded_by_text_in_last_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n text  @bob]")[1].children

    replace_func = Mock()

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE,
    )
    assert result == tokens

    replace_func.assert_not_called()


def test_replace_tag_tokens_only_of_type_in_line_strategy_doesnt_replace_multiple_void_children_in_first_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("@bob @john\nsecond line")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE,
    )
    assert result == [replacement, tokens[1], replacement] + tokens[3:]


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_multiple_void_children_in_middle_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n@bob @john\nsecond line")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE,
    )
    assert result == tokens[:2] + [replacement, tokens[3], replacement] + tokens[5:]


def test_replace_tag_tokens_only_of_type_in_line_strategy_replaces_multiple_void_children_in_last_line(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("first line\n@bob @john")[1].children

    replacement = Token(type="test", tag="t", nesting=0)

    def replace_func(tokens: list[Token], stack: list[Token]) -> list[Token]:
        assert len(tokens) == 1
        assert tokens[0].type == "mention"
        assert stack == []

        return [replacement]

    result = replace_tag_tokens(
        tokens,
        "misago-mention",
        replace_func,
        strategy=ReplaceTokensStrategy.ONLY_OF_TYPE_IN_LINE,
    )
    assert result == tokens[:2] + [replacement, tokens[3], replacement]
