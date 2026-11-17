from ..parse import parse, parse_to_plaintext


def test_parse_returns_parsing_result(db):
    result = parse("Hello world!")

    assert result.markup == "Hello world!"
    assert result.html == "<p>Hello world!</p>"
    assert result.text == "Hello world!"
    assert result.metadata == {}


def test_parse_to_plaintext_returns_text(db):
    result = parse_to_plaintext("Hello @user")
    assert result == "Hello @user"
