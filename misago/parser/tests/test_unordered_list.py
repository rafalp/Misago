def test_unordered_list(parse_markup):
    result = parse_markup("- Lorem")
    assert result == [
        {
            "type": "list",
            "ordered": False,
            "items": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Lorem",
                        },
                    ],
                    "items": [],
                },
            ],
        }
    ]


def test_unordered_list_with_multiple_items(parse_markup):
    result = parse_markup("- Lorem\n- Ipsum\n- Dolor")
    assert result == [
        {
            "type": "list",
            "ordered": False,
            "items": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Lorem",
                        },
                    ],
                    "items": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Ipsum",
                        },
                    ],
                    "items": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Dolor",
                        },
                    ],
                    "items": [],
                },
            ],
        }
    ]


def test_unordered_list_with_asterisk(parse_markup):
    result = parse_markup("- Lorem\n* Ipsum")
    assert result == [
        {
            "type": "list",
            "ordered": False,
            "items": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Lorem",
                        },
                    ],
                    "items": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Ipsum",
                        },
                    ],
                    "items": [],
                },
            ],
        }
    ]


def test_unordered_list_with_indent(parse_markup):
    result = parse_markup("  - Lorem\n  * Ipsum")
    assert result == [
        {
            "type": "list",
            "ordered": False,
            "items": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Lorem",
                        },
                    ],
                    "items": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Ipsum",
                        },
                    ],
                    "items": [],
                },
            ],
        }
    ]


def test_unordered_list_with_separating_blank_lines(parse_markup):
    result = parse_markup("  - Lorem\n\n\n  * Ipsum")
    assert result == [
        {
            "type": "list",
            "ordered": False,
            "items": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Lorem",
                        },
                    ],
                    "items": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Ipsum",
                        },
                    ],
                    "items": [],
                },
            ],
        }
    ]
