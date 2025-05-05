def test_short_image_markdown(parse_to_html):
    html = parse_to_html("!(https://placecats.com/300/200)")
    assert html == '<p><img src="https://placecats.com/300/200" alt=""></p>'


def test_short_image_markdown_with_title(parse_to_html):
    html = parse_to_html('!(https://placecats.com/300/200 "Cute Kat!")')
    assert html == (
        '<p><img src="https://placecats.com/300/200" alt="" title="Cute Kat!"></p>'
    )


def test_short_image_markdown_breaks_word(parse_to_html):
    html = parse_to_html('Lorem!(https://placecats.com/300/200 "Cute Kat!")Ipsum')
    assert html == (
        "<p>"
        "Lorem"
        '<img src="https://placecats.com/300/200" alt="" title="Cute Kat!">'
        "Ipsum"
        "</p>"
    )
