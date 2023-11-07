from ..parser import parse


def test_single_line_spoiler(request_mock, user, snapshot):
    text = "[spoiler]Daenerys and Jon live happily ever after![/spoiler]"
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]


def test_spoiler_can_contain_bbcode_or_markdown(request_mock, user, snapshot):
    text = "[spoiler]Sit **amet** [u]elit[/u].[/spoiler]"
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]


def test_multi_line_spoiler(request_mock, user, snapshot):
    text = """
[spoiler]
Sit amet elit.

Another line.
[/spoiler]
"""
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]


def test_spoilers_can_be_nested(request_mock, user, snapshot):
    text = """
[spoiler]
Sit amet elit.
[spoiler]Nested spoiler[/spoiler]
[/spoiler]
"""
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]


# Regression test for weird edge case in which hr gets moved outside of spoiler
def test_spoilers_can_contain_hr_markdown(request_mock, user, snapshot):
    text = """
[spoiler]
Sit amet elit.
- - - - -
Another line.
[/spoiler]
"""
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]
