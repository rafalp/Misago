from ..parser import parse


def test_single_line_quote(request_mock, user, snapshot):
    text = "[quote]Sit amet elit.[/quote]"
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]


def test_single_line_authored_quote(request_mock, user, snapshot):
    text = '[quote="@Bob"]Sit amet elit.[/quote]'
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]


def test_single_line_authored_quote_without_quotations(request_mock, user, snapshot):
    text = "[quote=@Bob]Sit amet elit.[/quote]"
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]


def test_quote_can_contain_bbcode_or_markdown(request_mock, user, snapshot):
    text = "[quote]Sit **amet** [u]elit[/u].[/quote]"
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]


def test_multi_line_quote(request_mock, user, snapshot):
    text = """
[quote]
Sit amet elit.

Another line.
[/quote]
"""
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]


def test_quotes_can_be_nested(request_mock, user, snapshot):
    text = """
[quote]
Sit amet elit.
[quote]Nested quote[/quote]
[/quote]
"""
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]


# Regression test for weird edge case in which hr gets moved outside of quote
def test_quotes_can_contain_hr_markdown(request_mock, user, snapshot):
    text = """
[quote]
Sit amet elit.
- - - - -
Another line.
[/quote]
"""
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]
