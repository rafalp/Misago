def test_empty_quote_is_removed(parse_markup):
    result = parse_markup("> ")
    assert result == []


def test_blank_quote_is_removed(parse_markup):
    result = parse_markup(">      ")
    assert result == []


def test_single_line_quote(parse_markup):
    result = parse_markup("> Lorem ipsum")
    assert result == [
        {
            "type": "quote",
            "children": [
                {
                    "type": "paragraph",
                    "children": [
                        {"type": "text", "text": "Lorem ipsum"},
                    ],
                },
            ],
        }
    ]


def test_multi_line_quote(parse_markup):
    result = parse_markup("> Lorem ipsum\n> Dolor met")
    assert result == [
        {
            "type": "quote",
            "children": [
                {
                    "type": "paragraph",
                    "children": [
                        {"type": "text", "text": "Lorem ipsum"},
                        {"type": "line-break"},
                        {"type": "text", "text": "Dolor met"},
                    ],
                },
            ],
        }
    ]


def test_multi_paragraph_quote(parse_markup):
    result = parse_markup("> Lorem ipsum\n>\n> Dolor met")
    assert result == [
        {
            "type": "quote",
            "children": [
                {
                    "type": "paragraph",
                    "children": [
                        {"type": "text", "text": "Lorem ipsum"},
                    ],
                },
                {
                    "type": "paragraph",
                    "children": [
                        {"type": "text", "text": "Dolor met"},
                    ],
                },
            ],
        }
    ]


def test_nested_quote(parse_markup):
    result = parse_markup("> Lorem ipsum\n> > Sit amet\n> Dolor met")
    assert result == [
        {
            "type": "quote",
            "children": [
                {
                    "type": "paragraph",
                    "children": [
                        {"type": "text", "text": "Lorem ipsum"},
                    ],
                },
                {
                    "type": "quote",
                    "children": [
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "Sit amet"},
                            ],
                        },
                    ],
                },
                {
                    "type": "paragraph",
                    "children": [
                        {"type": "text", "text": "Dolor met"},
                    ],
                },
            ],
        }
    ]
