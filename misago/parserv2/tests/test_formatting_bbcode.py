def test_bold_bbcode(parse_to_html):
    html = parse_to_html("Hello [b]world[/b]!")
    assert html == "<p>Hello <b>world</b>!</p>"


def test_italics_bbcode(parse_to_html):
    html = parse_to_html("Hello [i]world[/i]!")
    assert html == "<p>Hello <i>world</i>!</p>"


def test_underline_bbcode(parse_to_html):
    html = parse_to_html("Hello [u]world[/u]!")
    assert html == "<p>Hello <u>world</u>!</p>"


def test_strikethrough_bbcode(parse_to_html):
    html = parse_to_html("Hello [s]world[/s]!")
    assert html == "<p>Hello <del>world</del>!</p>"


def test_nested_formatting_bbcode(parse_to_html):
    html = parse_to_html("Hello [b]wo[u]r[/u]ld[/b]!")
    assert html == "<p>Hello <b>wo<u>r</u>ld</b>!</p>"


def test_formatting_bbcode_parses_contents(parse_to_html):
    html = parse_to_html("Hello [b]<http://example.com>[/b]!")
    assert html == (
        "<p>Hello <b>"
        '<a href="http://example.com" target="_blank">http://example.com</a>'
        "</b>!</p>"
    )
