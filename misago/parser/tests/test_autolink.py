def test_autolink(parse_markup):
    result = parse_markup("Hello <https://image.com/>!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "auto-link",
                    "image": False,
                    "href": "https://image.com/",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_autolink_image(parse_markup):
    result = parse_markup("Hello <!https://image.com/>!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "auto-link",
                    "image": True,
                    "href": "https://image.com/",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_autolink_invalid_url(parse_markup):
    result = parse_markup("Hello <!invalid-url>!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello <!invalid-url>!"},
            ],
        }
    ]


def test_autolink_image_email_url(parse_markup):
    result = parse_markup("Hello <!lorem@ipsum.com>!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello <!lorem@ipsum.com>!"},
            ],
        }
    ]


def test_autolink_in_url_is_not_parsed(parse_markup):
    result = parse_markup("Hello [<!https://image.com/>](https://image.com/)!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "url",
                    "href": "https://image.com/",
                    "title": None,
                    "children": [
                        {"type": "text", "text": "<!https://image.com/>"},
                    ],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_autolink_in_url_bbcode_is_not_parsed(parse_markup):
    result = parse_markup("Hello [url=https://image.com/]<!https://image.com/>[/url]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "url-bbcode",
                    "href": "https://image.com/",
                    "children": [
                        {"type": "text", "text": "<!https://image.com/>"},
                    ],
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_auto_url(parse_markup):
    result = parse_markup("Hello https://image.com/ !")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "auto-url",
                    "href": "https://image.com/",
                },
                {"type": "text", "text": " !"},
            ],
        }
    ]
