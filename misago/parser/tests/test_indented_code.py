def test_indented_code(parse_markup):
    result = parse_markup(
        """
        Code:

            lorem ipsum
        """
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Code:"}],
        },
        {
            "type": "code-indented",
            "syntax": None,
            "code": "lorem ipsum",
        },
    ]


def test_indented_code_multiline(parse_markup):
    result = parse_markup(
        """
        Code:

            lorem ipsum
              dolor met
            sit amet
        """
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Code:"}],
        },
        {
            "type": "code-indented",
            "syntax": None,
            "code": "lorem ipsum\n  dolor met\nsit amet",
        },
    ]


def test_indented_code_is_continued_after_empty_lines(parse_markup):
    result = parse_markup(
        """
        Code:

            lorem ipsum

            sit amet
        """
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Code:"}],
        },
        {
            "type": "code-indented",
            "syntax": None,
            "code": "lorem ipsum\n\nsit amet",
        },
    ]


def test_indented_code_is_continued_after_lines_with_spaces(parse_markup):
    result = parse_markup(
        """
        Code:

            lorem ipsum
  
            sit amet
        """
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Code:"}],
        },
        {
            "type": "code-indented",
            "syntax": None,
            "code": "lorem ipsum\n\nsit amet",
        },
    ]


def test_indented_code_preserves_escaping_characters(parse_markup):
    result = parse_markup(
        """
        Code:

            lorem \+ipsum
        """
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Code:"}],
        },
        {
            "type": "code-indented",
            "syntax": None,
            "code": "lorem \+ipsum",
        },
    ]


def test_indented_code_preserves_inline_code(parse_markup):
    result = parse_markup(
        """
        Code:

            `ipsum`
        """
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Code:"}],
        },
        {
            "type": "code-indented",
            "syntax": None,
            "code": "`ipsum`",
        },
    ]
