def test_link_in_url_bbcode_is_not_parsed(parse_to_html):
    html = parse_to_html("[url=example.com][test](example.com)[/url]")
    assert html == (
        "<p>"
        '<a href="example.com" rel="external nofollow noopener" target="_blank">'
        "[test](example.com)"
        "</a>"
        "</p>"
    )
