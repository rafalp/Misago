from ..escape import escape, unescape


def test_escape():
    assert escape("hello [world]") == "hello \\[world\\]"


def test_escape_specified():
    assert escape("hello *\\[world]*", "[]") == "hello *\\\\\\[world\\]*"


def test_escape_slashes():
    assert escape("hello \\[world]") == "hello \\\\\\[world\\]"


def test_unescape():
    assert unescape("he\\llo \\\\\\[world\\] hue\\") == "he\\llo \\[world] hue\\"
