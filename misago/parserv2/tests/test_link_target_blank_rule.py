def test_markdown_link_has_target_blank_set(parse_to_html):
    html = parse_to_html("[example](http://example.com)")
    assert html == ('<p><a href="http://example.com" target="_blank">example</a></p>')


def test_autolink_has_target_blank_set(parse_to_html):
    html = parse_to_html("<http://example.com>")
    assert html == (
        '<p><a href="http://example.com" target="_blank">http://example.com</a></p>'
    )


def test_linkified_link_has_target_blank_set(parse_to_html):
    html = parse_to_html("http://example.com")
    assert html == (
        '<p><a href="http://example.com" target="_blank">http://example.com</a></p>'
    )
