def test_escape_special_character_in_atx_heading(parse_markup):
    result = parse_markup("\\# Lorem ipsum")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "# Lorem ipsum"},
            ],
        }
    ]


def test_escape_escape_character_in_atx_heading(parse_markup):
    result = parse_markup("\\\\# Lorem ipsum")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "\# Lorem ipsum"},
            ],
        }
    ]


def test_escape_special_character_in_inline_code(parse_markup):
    result = parse_markup("Lorem ipsum \\`dolor\\` met.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Lorem ipsum `dolor` met."},
            ],
        }
    ]


def test_escape_skips_regular_characters(parse_markup):
    result = parse_markup("Lorem ipsum \\met.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Lorem ipsum \\met."},
            ],
        }
    ]
