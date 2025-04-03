def test_blockquotes_are_replaced_with_misago_quotes(parse_to_html):
    html = parse_to_html("> Hello world")
    assert html == ("<misago-quote>" "\n<p>Hello world</p>" "\n</misago-quote>")
