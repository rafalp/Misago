def test_markdown_link_has_target_blank_set(parse_to_html):
    html = parse_to_html("[example](http://example.com)")
    assert html == (
        "<p>"
        '<a href="http://example.com" rel="external nofollow noopener" target="_blank">'
        "example"
        "</a>"
        "</p>"
    )


def test_bbcode_url_has_target_blank_set(parse_to_html):
    html = parse_to_html("[url]http://example.com[/url]")
    assert html == (
        "<p>"
        "<a "
        'href="http://example.com" '
        'rel="external nofollow noopener" '
        'target="_blank" '
        'misago-rich-text="autolink"'
        ">"
        "example.com"
        "</a>"
        "</p>"
    )


def test_autolink_has_target_blank_set(parse_to_html):
    html = parse_to_html("<http://example.com>")
    assert html == (
        "<p>"
        "<a "
        'href="http://example.com" '
        'rel="external nofollow noopener" '
        'target="_blank" '
        'misago-rich-text="autolink"'
        ">"
        "example.com"
        "</a>"
        "</p>"
    )


def test_linkified_link_has_target_blank_set(parse_to_html):
    html = parse_to_html("http://example.com")
    assert html == (
        "<p>"
        "<a "
        'href="http://example.com" '
        'rel="external nofollow noopener" '
        'target="_blank" '
        'misago-rich-text="autolink"'
        ">"
        "example.com"
        "</a>"
        "</p>"
    )
