def test_image(parse_markup):
    result = parse_markup("Hello !(https://image.com/img.jpg)!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image",
                    "alt": None,
                    "title": None,
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_with_alt_text(parse_markup):
    result = parse_markup("Hello ![Image Alt](https://image.com/img.jpg)!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image",
                    "alt": "Image Alt",
                    "title": None,
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_alt_text_whitespace_is_stripped(parse_markup):
    result = parse_markup("Hello ![  Image Alt   ](https://image.com/img.jpg)!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image",
                    "alt": "Image Alt",
                    "title": None,
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_alt_text_is_empty(parse_markup):
    result = parse_markup("Hello ![](https://image.com/img.jpg)!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image",
                    "alt": None,
                    "title": None,
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_alt_text_is_not_parsed(parse_markup):
    result = parse_markup("Hello ![*Image Alt*](https://image.com/img.jpg)!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image",
                    "alt": "*Image Alt*",
                    "title": None,
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_alt_text_reserved_tokens_are_reversed(parse_markup):
    result = parse_markup("Hello ![`Image`](https://image.com/img.jpg)!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image",
                    "alt": "`Image`",
                    "title": None,
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_with_title(parse_markup):
    result = parse_markup('Hello !(https://image.com/img.jpg "Lorem ipsum")!')
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image",
                    "alt": None,
                    "title": "Lorem ipsum",
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_title_whitespace_is_stripped(parse_markup):
    result = parse_markup(
        'Hello !(https://image.com/img.jpg     "   Lorem ipsum  "   )!'
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image",
                    "alt": None,
                    "title": "Lorem ipsum",
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_title_is_empty(parse_markup):
    result = parse_markup('Hello !(https://image.com/img.jpg "")!')
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image",
                    "alt": None,
                    "title": None,
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_title_is_not_parsed(parse_markup):
    result = parse_markup('Hello !(https://image.com/img.jpg "*Lorem ipsum*")!')
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image",
                    "alt": None,
                    "title": "*Lorem ipsum*",
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_title_reserved_tokens_are_reversed(parse_markup):
    result = parse_markup('Hello !(https://image.com/img.jpg "`Image`")!')
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image",
                    "alt": None,
                    "title": "`Image`",
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_with_invalid_url(parse_markup):
    result = parse_markup("Hello !(invalid url)!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello !(invalid url)!"},
            ],
        }
    ]


def test_image_with_email_url(parse_markup):
    result = parse_markup("Hello !(lorem@ipsum.com).")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello !(lorem@ipsum.com)."},
            ],
        }
    ]


def test_image_with_empty_url(parse_markup):
    result = parse_markup("Hello !().")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello !()."},
            ],
        }
    ]


def test_image_with_alt_text_next_to_another_image_with_alt_text(parse_markup):
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
                    "title": None,
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": " "},
                {
                    "type": "image",
                    "alt": "Other Alt",
                    "title": None,
                    "src": "https://image.com/other.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_bbcode(parse_markup):
    result = parse_markup("Hello [img]https://image.com/img.jpg[/img]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image-bbcode",
                    "alt": None,
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_bbcode_url_whitespace_is_stripped(parse_markup):
    result = parse_markup("Hello [img]   https://image.com/img.jpg  [/img]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image-bbcode",
                    "alt": None,
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_bbcode_with_invalid_url(parse_markup):
    result = parse_markup("Hello [img] invalid url [/img]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello [img] invalid url [/img]!"},
            ],
        }
    ]


def test_image_bbcode_with_email_url(parse_markup):
    result = parse_markup("Hello [img]lorem@ipsum.com[/img]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello [img]lorem@ipsum.com[/img]!"},
            ],
        }
    ]


def test_image_bbcode_with_alt_text(parse_markup):
    result = parse_markup("Hello [img=https://image.com/img.jpg]alt text[/img]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image-bbcode",
                    "alt": "alt text",
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_bbcode_alt_text_whitespace_is_striped(parse_markup):
    result = parse_markup("Hello [img=https://image.com/img.jpg]  alt text    [/img]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image-bbcode",
                    "alt": "alt text",
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_bbcode_alt_text_is_not_parsed(parse_markup):
    result = parse_markup("Hello [img=https://image.com/img.jpg]**alt text**[/img]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image-bbcode",
                    "alt": "**alt text**",
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_bbcode_alt_text_reserved_patterns_are_reversed(parse_markup):
    result = parse_markup("Hello [img=https://image.com/img.jpg]`alt text`[/img]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image-bbcode",
                    "alt": "`alt text`",
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_bbcode_with_alt_text_url_is_trimmed(parse_markup):
    result = parse_markup("Hello [img='  https://image.com/img.jpg' ]alt text[/img]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "image-bbcode",
                    "alt": "alt text",
                    "src": "https://image.com/img.jpg",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_image_bbcode_with_alt_text_empty_url(parse_markup):
    result = parse_markup("Hello [img=]alt text[/img]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello [img=]alt text[/img]!"},
            ],
        }
    ]


def test_image_bbcode_with_alt_text_invalid_url(parse_markup):
    result = parse_markup("Hello [img=invalid url]alt text[/img]!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello [img=invalid url]alt text[/img]!"},
            ],
        }
    ]
