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
