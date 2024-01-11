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
