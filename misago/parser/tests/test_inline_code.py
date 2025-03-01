def test_inline_code(parse_markup):
    result = parse_markup("Hello `world`.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {"type": "code-inline", "code": "world"},
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
                {"type": "code-inline", "code": "world"},
                {"type": "text", "text": ", how's "},
                {"type": "code-inline", "code": "going"},
                {"type": "text", "text": "?"},
            ],
        }
    ]


def test_inline_code_linebreak_is_replaced_with_space(parse_markup):
    result = parse_markup("Hello `lorem\nipsum`.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {"type": "code-inline", "code": "lorem ipsum"},
                {"type": "text", "text": "."},
            ],
        }
    ]


def test_inline_code_multiple_linebreaks_dont_match(parse_markup):
    result = parse_markup("Hello `lorem\n\n\n\nipsum`.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello `lorem"},
            ],
        },
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "ipsum`."},
            ],
        },
    ]


def test_inline_code_content_is_skipped_by_block_parser(parse_markup):
    result = parse_markup("Hello `[quote]Text[/quote]`.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {"type": "code-inline", "code": "[quote]Text[/quote]"},
                {"type": "text", "text": "."},
            ],
        }
    ]


def test_inline_code_content_is_skipped_by_inline_parser(parse_markup):
    result = parse_markup("Hello `<http://misago-project.org>`.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {"type": "code-inline", "code": "<http://misago-project.org>"},
                {"type": "text", "text": "."},
            ],
        }
    ]


def test_inline_code_preserves_escape_strings(parse_markup):
    result = parse_markup("Hello `wor\+ld`.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {"type": "code-inline", "code": "wor\+ld"},
                {"type": "text", "text": "."},
            ],
        }
    ]


def test_inline_code_maintains_escaped_inline_character(parse_markup):
    result = parse_markup("This is how: `\`escaped text\``.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "This is how: "},
                {"type": "code-inline", "code": "`escaped text`"},
                {"type": "text", "text": "."},
            ],
        }
    ]
