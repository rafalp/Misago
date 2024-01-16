def test_inline_bbcode_with_text(parse_markup):
    result = parse_markup("Hello [b]guest[/b]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "bold-bbcode",
                    "children": [
                        {"type": "text", "text": "guest"},
                    ],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_inline_bbcode_with_new_line(parse_markup):
    result = parse_markup("Hello [b]guest\nname[/b]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "bold-bbcode",
                    "children": [
                        {"type": "text", "text": "guest"},
                        {"type": "line-break"},
                        {"type": "text", "text": "name"},
                    ],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_inline_bbcode_without_content_is_removed(parse_markup):
    result = parse_markup("Hello [b][/b]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello !"},
            ],
        }
    ]


def test_inline_bbcode_with_only_whitespaces_is_removed(parse_markup):
    result = parse_markup("Hello [b] \n  [/b]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello !"},
            ],
        }
    ]


def test_inline_bbcode_with_invalid_parent_is_unwrapped(parse_markup):
    result = parse_markup("Hello [sub]Bob [sup]Doe[/sup][/sub]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "subscript-bbcode",
                    "children": [
                        {"type": "text", "text": "Bob Doe"},
                    ],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_bold_bbcode(parse_markup):
    result = parse_markup("Hello [b]guest[/b]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "bold-bbcode",
                    "children": [
                        {"type": "text", "text": "guest"},
                    ],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_italics_bbcode(parse_markup):
    result = parse_markup("Hello [i]guest[/i]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "italics-bbcode",
                    "children": [
                        {"type": "text", "text": "guest"},
                    ],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_underline_bbcode(parse_markup):
    result = parse_markup("Hello [u]guest[/u]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "underline-bbcode",
                    "children": [
                        {"type": "text", "text": "guest"},
                    ],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_strikethrough_bbcode(parse_markup):
    result = parse_markup("Hello [s]guest[/s]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "strikethrough-bbcode",
                    "children": [
                        {"type": "text", "text": "guest"},
                    ],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_superscript_bbcode(parse_markup):
    result = parse_markup("Hello [sup]guest[/sup]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "superscript-bbcode",
                    "children": [
                        {"type": "text", "text": "guest"},
                    ],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_subscript_bbcode(parse_markup):
    result = parse_markup("Hello [sub]guest[/sub]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "subscript-bbcode",
                    "children": [
                        {"type": "text", "text": "guest"},
                    ],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]
