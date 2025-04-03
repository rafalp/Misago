def test_parser_escapes_html(parse_to_html):
    html = parse_to_html("<p>text</p>")
    assert html.startswith("<p>&lt;p&gt;text&lt;/p&gt;</p>")
