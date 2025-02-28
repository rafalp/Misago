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


def test_indented_code_is_continued_after_empty_line(parse_markup):
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


def test_indented_code_unescapes_characters(parse_markup):
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
            "code": "lorem ipsum",
        },
    ]
