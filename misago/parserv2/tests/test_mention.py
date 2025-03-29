def test_mention(parse_to_html):
    html = parse_to_html("@John123")
    assert html == '<p><misago-mention username="John123"></p>'


def test_mention_is_not_parsed_in_link(parse_to_html):
    html = parse_to_html("[@John123](http://example.com)")
    assert html == '<p><a href="http://example.com" target="_blank">@John123</a></p>'
