from markdown_it.token import Token

from ..tokens import split_inline_token


def test_split_inline_token_splits_inline_token_by_single_tag(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("lorem\nipsum")
    assert tokens[1].type == "inline"

    split_tokens = split_inline_token(tokens[1], "br")
    assert len(split_tokens) == 3

    assert split_tokens[0].type == "inline"
    assert split_tokens[0].children[0].content == "lorem"
    assert split_tokens[1].type == "softbreak"
    assert split_tokens[2].type == "inline"
    assert split_tokens[2].children[0].content == "ipsum"


def test_split_inline_token_splits_inline_token_by_multiple_tags(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("lorem\nipsum\ndolor\nmet")
    assert tokens[1].type == "inline"

    split_tokens = split_inline_token(tokens[1], "br")
    assert len(split_tokens) == 7

    assert split_tokens[0].type == "inline"
    assert split_tokens[0].children[0].content == "lorem"
    assert split_tokens[1].type == "softbreak"
    assert split_tokens[2].type == "inline"
    assert split_tokens[2].children[0].content == "ipsum"
    assert split_tokens[3].type == "softbreak"
    assert split_tokens[4].type == "inline"
    assert split_tokens[4].children[0].content == "dolor"
    assert split_tokens[5].type == "softbreak"
    assert split_tokens[6].type == "inline"
    assert split_tokens[6].children[0].content == "met"


def test_split_inline_token_strips_spaces(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("lorem @ipsum dolor")
    assert tokens[1].type == "inline"

    split_tokens = split_inline_token(tokens[1], "misago-mention")
    assert len(split_tokens) == 3

    assert split_tokens[0].type == "inline"
    assert split_tokens[0].children[0].content == "lorem"
    assert split_tokens[1].type == "mention"
    assert split_tokens[2].type == "inline"
    assert split_tokens[2].children[0].content == "dolor"


def test_split_inline_token_strips_softbreaks(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("lorem \n @ipsum \n dolor")
    assert tokens[1].type == "inline"

    split_tokens = split_inline_token(tokens[1], "misago-mention")
    assert len(split_tokens) == 3

    assert split_tokens[0].type == "inline"
    assert split_tokens[0].children[0].content == "lorem"
    assert split_tokens[1].type == "mention"
    assert split_tokens[2].type == "inline"
    assert split_tokens[2].children[0].content == "dolor"


def test_split_inline_token_strips_empty_text_tokens(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("lorem   @ipsum    @dolor   met")
    assert tokens[1].type == "inline"

    split_tokens = split_inline_token(tokens[1], "misago-mention")
    assert len(split_tokens) == 4

    assert split_tokens[0].type == "inline"
    assert split_tokens[0].children[0].content == "lorem"
    assert split_tokens[1].type == "mention"
    assert split_tokens[2].type == "mention"
    assert split_tokens[3].type == "inline"
    assert split_tokens[3].children[0].content == "met"


def test_split_inline_token_strips_softbreaks(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("lorem   @ipsum\n@dolor   met")
    assert tokens[1].type == "inline"

    split_tokens = split_inline_token(tokens[1], "misago-mention")
    assert len(split_tokens) == 4

    assert split_tokens[0].type == "inline"
    assert split_tokens[0].children[0].content == "lorem"
    assert split_tokens[1].type == "mention"
    assert split_tokens[2].type == "mention"
    assert split_tokens[3].type == "inline"
    assert split_tokens[3].children[0].content == "met"


def test_split_inline_token_strips_hardbreaks(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("lorem   @ipsum  \n  @dolor   met")
    assert tokens[1].type == "inline"

    split_tokens = split_inline_token(tokens[1], "misago-mention")
    assert len(split_tokens) == 4

    assert split_tokens[0].type == "inline"
    assert split_tokens[0].children[0].content == "lorem"
    assert split_tokens[1].type == "mention"
    assert split_tokens[2].type == "mention"
    assert split_tokens[3].type == "inline"
    assert split_tokens[3].children[0].content == "met"
