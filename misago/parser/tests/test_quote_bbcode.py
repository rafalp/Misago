def test_quote_bbcode_without_args(parse_to_html):
    html = parse_to_html("[quote]\nhello world\n[/quote]")
    assert html == "<misago-quote>\n<p>hello world</p>\n</misago-quote>"


def test_quote_bbcode_with_empty_args(parse_to_html):
    html = parse_to_html("[quote=]\nhello world\n[/quote]")
    assert html == "<misago-quote>\n<p>hello world</p>\n</misago-quote>"


def test_quote_bbcode_with_blank_args(parse_to_html):
    html = parse_to_html("[quote=   ]\nhello world\n[/quote]")
    assert html == "<misago-quote>\n<p>hello world</p>\n</misago-quote>"


def test_quote_bbcode_with_empty_quoted_args(parse_to_html):
    html = parse_to_html('[quote=""]\nhello world\n[/quote]')
    assert html == "<misago-quote>\n<p>hello world</p>\n</misago-quote>"


def test_quote_bbcode_with_blank_quoted_args(parse_to_html):
    html = parse_to_html('[quote="   "]\nhello world\n[/quote]')
    assert html == "<misago-quote>\n<p>hello world</p>\n</misago-quote>"


def test_quote_bbcode_with_info_arg(parse_to_html):
    html = parse_to_html("[quote=test]\nhello world\n[/quote]")
    assert html == '<misago-quote info="test">\n<p>hello world</p>\n</misago-quote>'


def test_quote_bbcode_with_quoted_info_arg(parse_to_html):
    html = parse_to_html('[quote="test"]\nhello world\n[/quote]')
    assert html == '<misago-quote info="test">\n<p>hello world</p>\n</misago-quote>'


def test_quote_bbcode_with_escaped_info_arg(parse_to_html):
    html = parse_to_html("[quote=lorem\\!ipsum]\nhello world\n[/quote]")
    assert (
        html == '<misago-quote info="lorem!ipsum">\n<p>hello world</p>\n</misago-quote>'
    )


def test_quote_bbcode_with_valid_user_and_post_args(parse_to_html):
    html = parse_to_html("[quote=John; post:2137]\nhello world\n[/quote]")
    assert html == (
        '<misago-quote user="John" post="2137">\n<p>hello world</p>\n</misago-quote>'
    )


def test_quote_bbcode_with_quoted_valid_user_and_post_args(parse_to_html):
    html = parse_to_html('[quote="John; post:2137"]\nhello world\n[/quote]')
    assert html == (
        '<misago-quote user="John" post="2137">\n<p>hello world</p>\n</misago-quote>'
    )


def test_quote_bbcode_with_escaped_valid_user_and_post_args(parse_to_html):
    html = parse_to_html("[quote=John\\; post:2137]\nhello world\n[/quote]")
    assert html == (
        '<misago-quote info="John; post:2137">\n<p>hello world</p>\n</misago-quote>'
    )


def test_quote_bbcode_with_valid_user_and_invalid_post_args(parse_to_html):
    html = parse_to_html("[quote=John; post:invalid]\nhello world\n[/quote]")
    assert html == (
        '<misago-quote info="John; post:invalid">\n<p>hello world</p>\n</misago-quote>'
    )


def test_quote_bbcode_without_args_single_line(parse_to_html):
    html = parse_to_html("[quote]hello world[/quote]")
    assert html == "<misago-quote>\n<p>hello world</p>\n</misago-quote>"


def test_quote_bbcode_with_info_arg_single_line(parse_to_html):
    html = parse_to_html("[quote=test]hello world[/quote]")
    assert html == '<misago-quote info="test">\n<p>hello world</p>\n</misago-quote>'


def test_quote_bbcode_without_args_single_line_parses_inline(parse_to_html):
    html = parse_to_html("[quote]hello **world**[/quote]")
    assert html == (
        "<misago-quote>\n<p>hello <strong>world</strong></p>\n</misago-quote>"
    )
