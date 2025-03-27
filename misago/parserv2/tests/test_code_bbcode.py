def test_code_bbcode_without_args(parse_to_html):
    html = parse_to_html('[code]\nhello("world")\n[/code]')
    assert html == "<misago-code>hello(&quot;world&quot;)\n</misago-code>"


def test_code_bbcode_without_args_single_line(parse_to_html):
    html = parse_to_html('[code]hello("world")[/code]')
    assert html == "<misago-code>hello(&quot;world&quot;)</misago-code>"
