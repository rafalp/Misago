def test_code(parse_to_html):
    html = parse_to_html('    hello("world")')
    assert html == "<misago-code>hello(&quot;world&quot;)</misago-code>"
