def test_bold_bbcode_is_rendered(parse_to_html):
    html = parse_to_html("Hello [b]world[/b]!")
    assert html == "<p>Hello <b>world</b>!</p>"


def test_italics_bbcode_is_rendered(parse_to_html):
    html = parse_to_html("Hello [i]world[/i]!")
    assert html == "<p>Hello <i>world</i>!</p>"


def test_underline_bbcode_is_rendered(parse_to_html):
    html = parse_to_html("Hello [u]world[/u]!")
    assert html == "<p>Hello <u>world</u>!</p>"
