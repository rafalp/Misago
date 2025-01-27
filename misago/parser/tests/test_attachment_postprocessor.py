def test_attachment_is_only_block(parse_markup):
    result = parse_markup("<attachment=image.png:1>")
    assert result == [
        {
            "type": "attachment",
            "name": "image.png",
            "id": 1,
        },
    ]


def test_two_attachments_are_two_blocks(parse_markup):
    result = parse_markup("<attachment=image.png:1><attachment=image2.png:2>")
    assert result == [
        {
            "type": "attachment",
            "name": "image.png",
            "id": 1,
        },
        {
            "type": "attachment",
            "name": "image2.png",
            "id": 2,
        },
    ]


def test_attachment_splits_paragraph(parse_markup):
    result = parse_markup("Lorem<attachment=image.png:1>Ipsum")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Lorem"},
            ],
        },
        {
            "type": "attachment",
            "name": "image.png",
            "id": 1,
        },
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Ipsum"},
            ],
        },
    ]


def test_attachments_split_paragraph(parse_markup):
    result = parse_markup(
        "Lorem<attachment=image.png:1>Ipsum<attachment=image2.png:2>Dolor"
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Lorem"},
            ],
        },
        {
            "type": "attachment",
            "name": "image.png",
            "id": 1,
        },
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Ipsum"},
            ],
        },
        {
            "type": "attachment",
            "name": "image2.png",
            "id": 2,
        },
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Dolor"},
            ],
        },
    ]


def test_attachment_in_inline_block_is_only_block(parse_markup):
    result = parse_markup("**<attachment=image.png:1>**")
    assert result == [
        {
            "type": "attachment",
            "name": "image.png",
            "id": 1,
        },
    ]


def test_attachment_in_quote_block_is_only_block(parse_markup):
    result = parse_markup("[quote]<attachment=image.png:1>[/quote]")
    assert result == [
        {
            "type": "quote-bbcode",
            "author": None,
            "post": None,
            "children": [
                {
                    "type": "attachment",
                    "name": "image.png",
                    "id": 1,
                },
            ],
        },
    ]


def test_attachment_in_quote_block_splits_paragraph(parse_markup):
    result = parse_markup("[quote]Lorem<attachment=image.png:1>Ipsum[/quote]")
    assert result == [
        {
            "type": "quote-bbcode",
            "author": None,
            "post": None,
            "children": [
                {
                    "type": "paragraph",
                    "children": [
                        {"type": "text", "text": "Lorem"},
                    ],
                },
                {
                    "type": "attachment",
                    "name": "image.png",
                    "id": 1,
                },
                {
                    "type": "paragraph",
                    "children": [
                        {"type": "text", "text": "Ipsum"},
                    ],
                },
            ],
        },
    ]


def test_attachment_splits_paragraph_inline_pattern(parse_markup):
    result = parse_markup("**Lorem<attachment=image.png:1>Ipsum**")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {
                    "type": "strong",
                    "children": [
                        {"type": "text", "text": "Lorem"},
                    ],
                },
            ],
        },
        {
            "type": "attachment",
            "name": "image.png",
            "id": 1,
        },
        {
            "type": "paragraph",
            "children": [
                {
                    "type": "strong",
                    "children": [
                        {"type": "text", "text": "Ipsum"},
                    ],
                },
            ],
        },
    ]
