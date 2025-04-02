def test_markdown_link_has_external_nofollow_noopener_set(parse_to_html):
    html = parse_to_html("[example](http://example.com)")
    assert html == (
        "<p>"
        '<a href="http://example.com" rel="external nofollow noopener" target="_blank">'
        "example"
        "</a>"
        "</p>"
    )


def test_bbcode_url_has_external_nofollow_noopener_set(parse_to_html):
    html = parse_to_html("[url]http://example.com[/url]")
    assert html == (
        "<p>"
        '<a href="http://example.com" rel="external nofollow noopener" target="_blank">'
        "example.com"
        "</a>"
        "</p>"
    )


def test_autolink_has_external_nofollow_noopener_set(parse_to_html):
    html = parse_to_html("<http://example.com>")
    assert html == (
        "<p>"
        '<a href="http://example.com" rel="external nofollow noopener" target="_blank">'
        "example.com"
        "</a>"
        "</p>"
    )


def test_linkified_link_has_external_nofollow_noopener_set(parse_to_html):
    html = parse_to_html("http://example.com")
    assert html == (
        "<p>"
        '<a href="http://example.com" rel="external nofollow noopener" target="_blank">'
        "example.com"
        "</a>"
        "</p>"
    )
