from markdown_it.token import Token

from ..tokens import inline_token_strip


def print_contents(token: Token) -> str:
    content = ""

    for child in token.children:
        if child.type == "text":
            content += child.content
        if child.type in ("softbreak", "hardbreak"):
            content += "\n"

    return content


def test_inline_token_strip_strips_text_tokens_whitespace(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("Lorem [b]ipsum[/b] dolor")
    assert tokens[1].type == "inline"

    inline_token = tokens[1]
    inline_token.children[0].content = "   " + inline_token.children[0].content
    inline_token.children[-1].content += "   "
    assert print_contents(inline_token) == "   Lorem ipsum dolor   "

    inline_token = inline_token_strip(inline_token)
    assert print_contents(inline_token) == "Lorem ipsum dolor"


def test_inline_token_strip_strips_softbreak_tokens(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("Lorem [b]ipsum[/b] dolor")
    assert tokens[1].type == "inline"

    inline_token = tokens[1]
    inline_token.children.insert(0, Token(type="softbreak", tag="br", nesting=0))
    inline_token.children.append(Token(type="softbreak", tag="br", nesting=0))
    assert print_contents(inline_token) == "\nLorem ipsum dolor\n"

    inline_token = inline_token_strip(inline_token)
    assert print_contents(inline_token) == "Lorem ipsum dolor"


def test_inline_token_strip_strips_hardbreak_tokens(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("Lorem [b]ipsum[/b] dolor")
    assert tokens[1].type == "inline"

    inline_token = tokens[1]
    inline_token.children.insert(0, Token(type="hardbreak", tag="br", nesting=0))
    inline_token.children.append(Token(type="hardbreak", tag="br", nesting=0))
    assert print_contents(inline_token) == "\nLorem ipsum dolor\n"

    inline_token = inline_token_strip(inline_token)
    assert print_contents(inline_token) == "Lorem ipsum dolor"


def test_inline_token_strip_strips_softbreak_and_whitespace_tokens(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("Lorem [b]ipsum[/b] dolor")
    assert tokens[1].type == "inline"

    inline_token = tokens[1]
    inline_token.children[0].content = "   " + inline_token.children[0].content
    inline_token.children[-1].content += "   "
    inline_token.children.insert(0, Token(type="softbreak", tag="br", nesting=0))
    inline_token.children.insert(
        0, Token(type="text", tag="", content="   ", nesting=0)
    )
    inline_token.children.insert(0, Token(type="softbreak", tag="br", nesting=0))
    inline_token.children.insert(
        0, Token(type="text", tag="", content="   ", nesting=0)
    )
    inline_token.children.append(Token(type="softbreak", tag="br", nesting=0))
    inline_token.children.append(Token(type="text", tag="", content="   ", nesting=0))
    inline_token.children.append(Token(type="softbreak", tag="br", nesting=0))
    inline_token.children.append(Token(type="text", tag="", content="   ", nesting=0))
    assert print_contents(inline_token) == "   \n   \n   Lorem ipsum dolor   \n   \n   "

    inline_token = inline_token_strip(inline_token)
    assert print_contents(inline_token) == "Lorem ipsum dolor"


def test_inline_token_strip_strips_hardbreak_and_whitespace_tokens(parse_to_raw_tokens):
    tokens = parse_to_raw_tokens("Lorem [b]ipsum[/b] dolor")
    assert tokens[1].type == "inline"

    inline_token = tokens[1]
    inline_token.children[0].content = "   " + inline_token.children[0].content
    inline_token.children[-1].content += "   "
    inline_token.children.insert(0, Token(type="hardbreak", tag="br", nesting=0))
    inline_token.children.insert(
        0, Token(type="text", tag="", content="   ", nesting=0)
    )
    inline_token.children.insert(0, Token(type="hardbreak", tag="br", nesting=0))
    inline_token.children.insert(
        0, Token(type="text", tag="", content="   ", nesting=0)
    )
    inline_token.children.append(Token(type="hardbreak", tag="br", nesting=0))
    inline_token.children.append(Token(type="text", tag="", content="   ", nesting=0))
    inline_token.children.append(Token(type="hardbreak", tag="br", nesting=0))
    inline_token.children.append(Token(type="text", tag="", content="   ", nesting=0))
    assert print_contents(inline_token) == "   \n   \n   Lorem ipsum dolor   \n   \n   "

    inline_token = inline_token_strip(inline_token)
    assert print_contents(inline_token) == "Lorem ipsum dolor"


def test_inline_token_strip_returns_none_if_stripped_token_is_empty(
    parse_to_raw_tokens,
):
    tokens = parse_to_raw_tokens("Lorem")
    assert tokens[1].type == "inline"

    inline_token = tokens[1]
    inline_token.children[0].content = "   "
    assert inline_token_strip(inline_token) is None
