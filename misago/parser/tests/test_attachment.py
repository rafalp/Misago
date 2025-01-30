def test_attachment(parse_markup):
    result = parse_markup('Hello <attachment="image.png:1234">!')
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
            ],
        },
        {
            "type": "attachment-group",
            "children": [
                {
                    "type": "attachment",
                    "name": "image.png",
                    "slug": "image-png",
                    "id": 1234,
                },
            ],
        },
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "!"},
            ],
        },
    ]


def test_attachment_without_quotes_around_args(parse_markup):
    result = parse_markup("Hello <attachment=image.png:1234>!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
            ],
        },
        {
            "type": "attachment-group",
            "children": [
                {
                    "type": "attachment",
                    "name": "image.png",
                    "slug": "image-png",
                    "id": 1234,
                },
            ],
        },
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "!"},
            ],
        },
    ]


def test_attachment_with_spaces_in_args(parse_markup):
    result = parse_markup("Hello <attachment=   image.png   :  1234   >!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
            ],
        },
        {
            "type": "attachment-group",
            "children": [
                {
                    "type": "attachment",
                    "name": "image.png",
                    "slug": "image-png",
                    "id": 1234,
                },
            ],
        },
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "!"},
            ],
        },
    ]


def test_attachment_next_to_other_attachment(parse_markup):
    result = parse_markup("Hello <attachment=image.png:6><attachment=image2.png:7>")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
            ],
        },
        {
            "type": "attachment-group",
            "children": [
                {
                    "type": "attachment",
                    "name": "image.png",
                    "slug": "image-png",
                    "id": 6,
                },
                {
                    "type": "attachment",
                    "name": "image2.png",
                    "slug": "image2-png",
                    "id": 7,
                },
            ],
        },
    ]


def test_attachments_with_spaces_between(parse_markup):
    result = parse_markup("Hello <attachment=image.png:6>    <attachment=image2.png:7>")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
            ],
        },
        {
            "type": "attachment-group",
            "children": [
                {
                    "type": "attachment",
                    "name": "image.png",
                    "slug": "image-png",
                    "id": 6,
                },
                {
                    "type": "attachment",
                    "name": "image2.png",
                    "slug": "image2-png",
                    "id": 7,
                },
            ],
        },
    ]


def test_attachments_with_blank_lines_between(parse_markup):
    result = parse_markup(
        "Hello <attachment=image.png:6>    \n\nWorld <attachment=image2.png:7>"
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
            ],
        },
        {
            "type": "attachment-group",
            "children": [
                {
                    "type": "attachment",
                    "name": "image.png",
                    "slug": "image-png",
                    "id": 6,
                },
            ],
        },
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "World "},
            ],
        },
        {
            "type": "attachment-group",
            "children": [
                {
                    "type": "attachment",
                    "name": "image2.png",
                    "slug": "image2-png",
                    "id": 7,
                },
            ],
        },
    ]


def test_attachment_without_id_is_not_parsed(parse_markup):
    result = parse_markup("Hello <attachment=image.png>!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello <attachment=image.png>!"},
            ],
        }
    ]


def test_attachment_without_name_is_not_parsed(parse_markup):
    result = parse_markup("Hello <attachment=1234>!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello <attachment=1234>!"},
            ],
        }
    ]


def test_attachment_with_empty_name_is_not_parsed(parse_markup):
    result = parse_markup("Hello <attachment=:1234>!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello <attachment=:1234>!"},
            ],
        }
    ]


def test_attachment_with_empty_id_is_not_parsed(parse_markup):
    result = parse_markup("Hello <attachment=image.png:>!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello <attachment=image.png:>!"},
            ],
        }
    ]


def test_attachment_with_invalid_id_is_not_parsed(parse_markup):
    result = parse_markup("Hello <attachment=image.png:invalid>!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello <attachment=image.png:invalid>!"},
            ],
        }
    ]


def test_attachment_with_zero_id_is_not_parsed(parse_markup):
    result = parse_markup("Hello <attachment=image.png:0>!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello <attachment=image.png:0>!"},
            ],
        }
    ]


def test_attachment_with_negative_id_is_not_parsed(parse_markup):
    result = parse_markup("Hello <attachment=image.png:-123>!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello <attachment=image.png:-123>!"},
            ],
        }
    ]


def test_attachment_with_empty_args_is_not_parsed(parse_markup):
    result = parse_markup("Hello <attachment=:>!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello <attachment=:>!"},
            ],
        }
    ]


def test_attachment_with_too_many_args_is_not_parsed(parse_markup):
    result = parse_markup("Hello <attachment=image.png:extra:123>!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello <attachment=image.png:extra:123>!"},
            ],
        }
    ]
