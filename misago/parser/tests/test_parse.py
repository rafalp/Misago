from ..parse import parse


def test_parse_returns_parsing_result(db):
    result = parse("Hello world!")

    assert result.markup == "Hello world!"
    assert result.html == "<p>Hello world!</p>"
    assert result.text == "Hello world!"
    assert result.metadata == {}
