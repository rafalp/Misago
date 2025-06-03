def test_spoiler_bbcode_without_args(parse_to_html):
    html = parse_to_html("[spoiler]\nhello world\n[/spoiler]")
    assert html == "<misago-spoiler>\n<p>hello world</p>\n</misago-spoiler>"


def test_spoiler_bbcode_with_empty_args(parse_to_html):
    html = parse_to_html("[spoiler=]\nhello world\n[/spoiler]")
    assert html == "<misago-spoiler>\n<p>hello world</p>\n</misago-spoiler>"


def test_spoiler_bbcode_with_blank_args(parse_to_html):
    html = parse_to_html("[spoiler=   ]\nhello world\n[/spoiler]")
    assert html == "<misago-spoiler>\n<p>hello world</p>\n</misago-spoiler>"


def test_spoiler_bbcode_with_empty_quoted_args(parse_to_html):
    html = parse_to_html('[spoiler=""]\nhello world\n[/spoiler]')
    assert html == "<misago-spoiler>\n<p>hello world</p>\n</misago-spoiler>"


def test_spoiler_bbcode_with_blank_quoted_args(parse_to_html):
    html = parse_to_html('[spoiler="   "]\nhello world\n[/spoiler]')
    assert html == "<misago-spoiler>\n<p>hello world</p>\n</misago-spoiler>"


def test_spoiler_bbcode_with_info_arg(parse_to_html):
    html = parse_to_html("[spoiler=test]\nhello world\n[/spoiler]")
    assert html == '<misago-spoiler info="test">\n<p>hello world</p>\n</misago-spoiler>'


def test_spoiler_bbcode_with_quoted_info_arg(parse_to_html):
    html = parse_to_html('[spoiler="test"]\nhello world\n[/spoiler]')
    assert html == '<misago-spoiler info="test">\n<p>hello world</p>\n</misago-spoiler>'


def test_spoiler_bbcode_with_escaped_info_arg(parse_to_html):
    html = parse_to_html("[spoiler=lorem\\!ipsum]\nhello world\n[/spoiler]")
    assert (
        html
        == '<misago-spoiler info="lorem!ipsum">\n<p>hello world</p>\n</misago-spoiler>'
    )


def test_spoiler_bbcode_without_args_single_line(parse_to_html):
    html = parse_to_html("[spoiler]hello world[/spoiler]")
    assert html == "<misago-spoiler>\n<p>hello world</p>\n</misago-spoiler>"


def test_spoiler_bbcode_with_info_arg_single_line(parse_to_html):
    html = parse_to_html("[spoiler=test]hello world[/spoiler]")
    assert html == '<misago-spoiler info="test">\n<p>hello world</p>\n</misago-spoiler>'


def test_spoiler_bbcode_without_args_single_line_parses_inline(parse_to_html):
    html = parse_to_html("[spoiler]hello **world**[/spoiler]")
    assert html == (
        "<misago-spoiler>\n<p>hello <strong>world</strong></p>\n</misago-spoiler>"
    )
