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
                        {"type": "softbreak"},
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


def test_quote_with_indented_code(parse_markup):
    result = parse_markup(">     test")
    assert result == [
        {
            "type": "quote",
            "children": [
                {
                    "type": "code-indented",
                    "syntax": None,
                    "code": "test",
                },
            ],
        }
    ]


def test_quote_unescapes_text(parse_markup):
    result = parse_markup("> Lorem \*ipsum\*")
    assert result == [
        {
            "type": "quote",
            "children": [
                {
                    "type": "paragraph",
                    "children": [
                        {"type": "text", "text": "Lorem *ipsum*"},
                    ],
                },
            ],
        }
    ]


def test_quote_next_to_another(parse_markup):
    result = parse_markup("> Lorem ipsum\n\n> Dolor met")
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
        },
        {
            "type": "quote",
            "children": [
                {
                    "type": "paragraph",
                    "children": [
                        {"type": "text", "text": "Dolor met"},
                    ],
                },
            ],
        },
    ]