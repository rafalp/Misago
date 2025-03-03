def test_quote_bbcode(parse_markup):
    result = parse_markup("[quote]Hello world![/quote]")
    assert result == [
        {
            "type": "quote-bbcode",
            "user": None,
            "post": None,
            "info": None,
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Hello world!"}],
                },
            ],
        },
    ]


def test_quote_bbcode_with_empty_info(parse_markup):
    result = parse_markup("[quote=]Hello world![/quote]")
    assert result == [
        {
            "type": "quote-bbcode",
            "user": None,
            "post": None,
            "info": None,
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Hello world!"}],
                },
            ],
        },
    ]


def test_quote_bbcode_with_info(parse_markup):
    result = parse_markup("[quote=Dune, part 2]Hello world![/quote]")
    assert result == [
        {
            "type": "quote-bbcode",
            "user": None,
            "post": None,
            "info": [
                {"type": "text", "text": "Dune, part 2"},
            ],
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Hello world!"}],
                },
            ],
        },
    ]


def test_quote_bbcode_with_author_and_post(parse_markup):
    result = parse_markup("[quote=John; post:2137]Hello world![/quote]")
    assert result == [
        {
            "type": "quote-bbcode",
            "user": "John",
            "post": 2137,
            "info": None,
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Hello world!"}],
                },
            ],
        },
    ]


def test_quote_bbcode_with_author_and_empty_post(parse_markup):
    result = parse_markup("[quote=John; post:]Hello world![/quote]")
    assert result == [
        {
            "type": "quote-bbcode",
            "user": None,
            "post": None,
            "info": [
                {"type": "text", "text": "John; post:"},
            ],
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Hello world!"}],
                },
            ],
        },
    ]


def test_quote_bbcode_with_author_and_invalid_post(parse_markup):
    result = parse_markup("[quote=John; post:dsadsa]Hello world![/quote]")
    assert result == [
        {
            "type": "quote-bbcode",
            "user": None,
            "post": None,
            "info": [
                {"type": "text", "text": "John; post:dsadsa"},
            ],
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Hello world!"}],
                },
            ],
        },
    ]


def test_quote_bbcode_without_author_and_with_post(parse_markup):
    result = parse_markup("[quote=post:2137]Hello world![/quote]")
    assert result == [
        {
            "type": "quote-bbcode",
            "user": None,
            "post": None,
            "info": [
                {"type": "text", "text": "post:2137"},
            ],
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Hello world!"}],
                },
            ],
        },
    ]


def test_quote_bbcode_with_extra_post(parse_markup):
    result = parse_markup("[quote=John; post:1; post:3]Hello world![/quote]")
    assert result == [
        {
            "type": "quote-bbcode",
            "user": None,
            "post": None,
            "info": [
                {"type": "text", "text": "John; post:1; post:3"},
            ],
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Hello world!"}],
                },
            ],
        },
    ]


def test_quote_bbcode_with_space_around_post(parse_markup):
    result = parse_markup("[quote=John; post:  3]Hello world![/quote]")
    assert result == [
        {
            "type": "quote-bbcode",
            "user": "John",
            "post": 3,
            "info": None,
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Hello world!"}],
                },
            ],
        },
    ]


def test_quote_bbcode_strips_quotations_and_spaces_from_info(parse_markup):
    result = parse_markup('[quote="  Dune, part 2 "]Hello world![/quote]')
    assert result == [
        {
            "type": "quote-bbcode",
            "user": None,
            "post": None,
            "info": [
                {"type": "text", "text": "Dune, part 2"},
            ],
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Hello world!"}],
                },
            ],
        },
    ]


def test_quote_bbcode_unescapes_info(parse_markup):
    result = parse_markup('[quote="Dune, \\"part 2\\" "]Hello world![/quote]')
    assert result == [
        {
            "type": "quote-bbcode",
            "user": None,
            "post": None,
            "info": [
                {"type": "text", "text": 'Dune, "part 2"'},
            ],
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Hello world!"}],
                },
            ],
        },
    ]


def test_empty_quote_bbcode_is_removed_from_result(parse_markup):
    result = parse_markup("Lorem ipsum.[quote][/quote]")
    assert result == [
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Lorem ipsum."}],
        },
    ]


def test_blank_quote_bbcode_is_removed_from_result(parse_markup):
    result = parse_markup("Lorem ipsum.[quote]     [/quote]")
    assert result == [
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Lorem ipsum."}],
        },
    ]


def test_quote_bbcode_next_to_paragraph_is_parsed(parse_markup):
    result = parse_markup("Lorem ipsum.[quote]Dolor met![/quote]")
    assert result == [
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Lorem ipsum."}],
        },
        {
            "type": "quote-bbcode",
            "user": None,
            "post": None,
            "info": None,
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Dolor met!"}],
                },
            ],
        },
    ]
