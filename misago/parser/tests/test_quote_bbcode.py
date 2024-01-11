def test_quote_bbcode(parse_markup):
    result = parse_markup("[quote]Hello world![/quote]")
    assert result == [
        {
            "type": "quote-bbcode",
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


def test_quote_bbcode_next_to_paragraph_is_parsed(parse_markup):
    result = parse_markup("Lorem ipsum.[quote]Dolor met![/quote]")
    assert result == [
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Lorem ipsum."}],
        },
        {
            "type": "quote-bbcode",
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Dolor met!"}],
                },
            ],
        },
    ]
