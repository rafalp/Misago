def test_inline_code(parse_markup):
    result = parse_markup("Hello `world`.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {"type": "inline-code", "code": "world"},
                {"type": "text", "text": "."},
            ],
        }
    ]


def test_multiple_inline_code(parse_markup):
    result = parse_markup("Hello `world`, how's `going`?")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {"type": "inline-code", "code": "world"},
                {"type": "text", "text": ", how's "},
                {"type": "inline-code", "code": "going"},
                {"type": "text", "text": "?"},
            ],
        }
    ]


def test_inline_code_is_not_parsed(parse_markup):
    result = parse_markup("Hello `<http://misago-project.org>`.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {"type": "inline-code", "code": "<http://misago-project.org>"},
                {"type": "text", "text": "."},
            ],
        }
    ]
