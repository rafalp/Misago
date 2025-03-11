from ..highlighter import highlight_syntax


def test_highlight_syntax_highlights_code():
    assert highlight_syntax("python", 'print("hello!")')


def test_highlight_syntax_handles_invalid_syntax():
    result = highlight_syntax("invalid", 'print("<hello!>")')
    assert "<" not in result
    assert ">" not in result
    assert '"' not in result


def test_highlight_syntax_doesnt_wrap_code():
    result = highlight_syntax("python", 'print("hello!")')
    assert "<pre>" not in result
    assert "<code>" not in result
