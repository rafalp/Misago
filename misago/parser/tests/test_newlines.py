def test_softbreak_is_included_in_parsed_text(parse_to_html):
    html = parse_to_html("Lorem\nIpsum")
    assert html == "<p>Lorem<br>\nIpsum</p>"


def test_hardbreak_is_included_in_parsed_text(parse_to_html):
    html = parse_to_html("Lorem   \n   Ipsum")
    assert html == "<p>Lorem<br>\nIpsum</p>"
