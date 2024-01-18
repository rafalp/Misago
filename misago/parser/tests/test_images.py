def test_image_markdown(parse_markup):
    result = parse_markup("Hello !(https://image.com/img.jpg)!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image",
                    "alt": None,
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_with_alt_markdown(parse_markup):
    result = parse_markup("Hello ![Image Alt](https://image.com/img.jpg)!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image",
                    "alt": "Image Alt",
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_alt_whitespace_is_stripped(parse_markup):
    result = parse_markup("Hello ![  Image Alt   ](https://image.com/img.jpg)!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image",
                    "alt": "Image Alt",
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_alt_is_not_parsed(parse_markup):
    result = parse_markup("Hello ![*Image Alt*](https://image.com/img.jpg)!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image",
                    "alt": "*Image Alt*",
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_with_alt_markdown_next_to_another(parse_markup):
    result = parse_markup(
        "Hello ![Image Alt](https://image.com/img.jpg)"
        " ![Other Alt](https://image.com/other.jpg)!"
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image",
                    "alt": "Image Alt",
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": " "},
                {
                    "type": "image",
                    "alt": "Other Alt",
                    "src": "https://image.com/other.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]
