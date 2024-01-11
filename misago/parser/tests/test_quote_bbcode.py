def test_quote_bbcode(parse_markup):
    result = parse_markup("[quote]Hello world![/quote]")
    assert result == [
        {"type": "quote-bbcode-open"},
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Hello world!"}],
        },
        {"type": "quote-bbcode-close"},
    ]


def test_empty_quote_bbcode_is_removed_from_result(parse_markup):
    result = parse_markup("Lorem ipsum.[quote]Hello world![/quote]")
    assert result == [
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Lorem ipsum."}],
        },
    ]
