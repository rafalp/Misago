from ..parser import parse


def test_html_is_escaped(request_mock, user, snapshot):
    text = "Lorem <strong>ipsum!</strong>"
    result = parse(text, request_mock, user, minify=True)
    snapshot.assert_match(result["parsed_text"])


def test_parsed_text_is_minified(request_mock, user, snapshot):
    text = """
Lorem **ipsum** dolor met.

Sit amet elit.
"""
    result = parse(text, request_mock, user, minify=True)
    snapshot.assert_match(result["parsed_text"])
