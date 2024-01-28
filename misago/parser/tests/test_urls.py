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


def test_url_with_missing_closing_parenthesis_next_to_other_url(parse_markup):
    result = parse_markup(
        "Hello [link label](https://example.com/link "
        "[other link](https://example.com/other)!"
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello [link label]("},
                {
                    "type": "auto-url",
                    "href": "https://example.com/link",
                },
                {"type": "text", "text": " "},
                {
                    "type": "url",
                    "href": "https://example.com/other",
                    "children": [
                        {"type": "text", "text": "other link"},
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


def test_image_between_two_urls(parse_markup):
    result = parse_markup(
        "Hello [Lorem](https://image.com/) "
        "![Image Alt](https://image.com/image.jpg) "
        "[Ipsum](https://other.com/)!"
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "url",
                    "href": "https://image.com/",
                    "children": [{"type": "text", "text": "Lorem"}],
                },
                {"type": "text", "text": " "},
                {
                    "type": "image",
                    "alt": "Image Alt",
                    "src": "https://image.com/image.jpg",
                },
                {"type": "text", "text": " "},
                {
                    "type": "url",
                    "href": "https://other.com/",
                    "children": [{"type": "text", "text": "Ipsum"}],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_before_url(parse_markup):
    result = parse_markup(
        "Hello ![Image Alt](https://image.com/image.jpg) "
        "[Lorem](https://image.com/)!"
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image",
                    "alt": "Image Alt",
                    "src": "https://image.com/image.jpg",
                },
                {"type": "text", "text": " "},
                {
                    "type": "url",
                    "href": "https://image.com/",
                    "children": [{"type": "text", "text": "Lorem"}],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_after_url(parse_markup):
    result = parse_markup(
        "Hello [Lorem](https://image.com/) "
        "![Image Alt](https://image.com/image.jpg)!"
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "url",
                    "href": "https://image.com/",
                    "children": [{"type": "text", "text": "Lorem"}],
                },
                {"type": "text", "text": " "},
                {
                    "type": "image",
                    "alt": "Image Alt",
                    "src": "https://image.com/image.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_url_bbcode(parse_markup):
    result = parse_markup("Hello [url]https://image.com/img.jpg[/url]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "url-bbcode",
                    "href": "https://image.com/img.jpg",
                    "children": [],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_url_bbcode_url_whitespace_is_stripped(parse_markup):
    result = parse_markup("Hello [url]   https://image.com/img.jpg  [/url]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "url-bbcode",
                    "href": "https://image.com/img.jpg",
                    "children": [],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_url_bbcode_with_invalid_url(parse_markup):
    result = parse_markup("Hello [url] invalid url [/url]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello [url] invalid url [/url]!"},
            ],
        }
    ]


def test_url_bbcode_with_email_url(parse_markup):
    result = parse_markup("Hello [url]lorem@ipsum.com[/url]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "url-bbcode",
                    "href": "mailto:lorem@ipsum.com",
                    "children": [],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_url_bbcode_with_empty_url(parse_markup):
    result = parse_markup("Hello [url] [/url]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello [url] [/url]!"},
            ],
        }
    ]


def test_url_bbcode_with_children(parse_markup):
    result = parse_markup("Hello [url=example.com]Alt text[/url]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "url-bbcode",
                    "href": "example.com",
                    "children": [
                        {"type": "text", "text": "Alt text"},
                    ],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_url_bbcode_with_children_empty_url(parse_markup):
    result = parse_markup("Hello [url=]Alt text[/url]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello [url=]Alt text[/url]!"},
            ],
        }
    ]


def test_url_bbcode_with_children_invalid_url(parse_markup):
    result = parse_markup("Hello [url=invalid url]Alt text[/url]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello [url=invalid url]Alt text[/url]!"},
            ],
        }
    ]


def test_url_bbcode_children_are_parsed(parse_markup):
    result = parse_markup("Hello [url=example.com]Alt **text**[/url]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "url-bbcode",
                    "href": "example.com",
                    "children": [
                        {"type": "text", "text": "Alt "},
                        {
                            "type": "strong",
                            "children": [
                                {"type": "text", "text": "text"},
                            ],
                        },
                    ],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_url_bbcode_with_empty_children(parse_markup):
    result = parse_markup("Hello [url=example.com][/url]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello [url=example.com][/url]!"},
            ],
        }
    ]
