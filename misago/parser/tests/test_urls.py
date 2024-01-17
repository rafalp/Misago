def test_url(parse_markup):
    result = parse_markup("Hello [link label](https://image.com/)!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "url",
                    "href": "https://image.com/",
                    "children": [
                        {"type": "text", "text": "link label"},
                    ],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_url_with_image_with_alt_markdown(parse_markup):
    result = parse_markup(
        "Hello [![Image Alt](https://image.com/image.jpg)](https://image.com/)!"
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "url",
                    "href": "https://image.com/",
                    "children": [
                        {
                            "type": "image",
                            "alt": "Image Alt",
                            "src": "https://image.com/image.jpg",
                        },
                    ],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_two_urls_with_image_with_alt_markdown(parse_markup):
    result = parse_markup(
        "Hello [![Image Alt](https://image.com/image.jpg)](https://image.com/) "
        "[Image: ![Image Other](https://image.com/other.jpg)](https://other.com/)!"
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "url",
                    "href": "https://image.com/",
                    "children": [
                        {
                            "type": "image",
                            "alt": "Image Alt",
                            "src": "https://image.com/image.jpg",
                        },
                    ],
                },
                {"type": "text", "text": " "},
                {
                    "type": "url",
                    "href": "https://other.com/",
                    "children": [
                        {"type": "text", "text": "Image: "},
                        {
                            "type": "image",
                            "alt": "Image Other",
                            "src": "https://image.com/other.jpg",
                        },
                    ],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_url_with_parenthesis(parse_markup):
    result = parse_markup("Hello [link label](https://example.com/Link_(Film))!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "url",
                    "href": "https://example.com/Link_(Film)",
                    "children": [
                        {"type": "text", "text": "link label"},
                    ],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_url_with_multiple_parenthesis(parse_markup):
    result = parse_markup(
        "Hello [link label](https://example.com/Link_(Film)_(Comedy))!"
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "url",
                    "href": "https://example.com/Link_(Film)_(Comedy)",
                    "children": [
                        {"type": "text", "text": "link label"},
                    ],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_url_with_nested_parenthesis(parse_markup):
    result = parse_markup(
        "Hello [link label](https://example.com/Link_(Film_(Comedy)))!"
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "url",
                    "href": "https://example.com/Link_(Film_(Comedy))",
                    "children": [
                        {"type": "text", "text": "link label"},
                    ],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_url_with_missing_closing_parenthesis_is_trimmed_to_last_one(parse_markup):
    result = parse_markup("Hello [link label](https://example.com/Link_(Film_(Comedy)!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "url",
                    "href": "https://example.com/Link_(Film_(Comedy",
                    "children": [
                        {"type": "text", "text": "link label"},
                    ],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_url_with_extra_closing_parenthesis_excludes_them(parse_markup):
    result = parse_markup("Hello [link label](https://example.com/Link_(Film)))!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "url",
                    "href": "https://example.com/Link_(Film)",
                    "children": [
                        {"type": "text", "text": "link label"},
                    ],
                },
                {"type": "text", "text": ")!"},
            ],
        }
    ]
