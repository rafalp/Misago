def test_escaped_atx_heading(parse_markup):
    result = parse_markup("\\# Lorem ipsum")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "escape", "sign": "#"},
                {"type": "text", "text": " Lorem ipsum"},
            ],
        }
    ]


def test_escaped_inline_code(parse_markup):
    result = parse_markup("Lorem ipsum \\`dolor\\` met.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Lorem ipsum "},
                {"type": "escape", "sign": "`"},
                {"type": "text", "text": "dolor"},
                {"type": "escape", "sign": "`"},
                {"type": "text", "text": " met."},
            ],
        }
    ]


def test_escape_is_not_working_for_characters(parse_markup):
    result = parse_markup("Lorem ipsum \\met.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Lorem ipsum \\met."},
            ],
        }
    ]
