def test_url_bbcode(parse_to_html):
    html = parse_to_html("[url]example.com[/url]")
    assert html == (
        "<p>"
        "<a "
        'href="example.com" '
        'rel="external nofollow noopener" '
        'target="_blank" '
        'misago-rich-text="autolink"'
        ">"
        "example.com"
        "</a>"
        "</p>"
    )


def test_url_bbcode_without_content(parse_to_html):
    html = parse_to_html("[url][/url]")
    assert html == "<p>[url][/url]</p>"


def test_url_bbcode_with_blank_content(parse_to_html):
    html = parse_to_html("[url]   [/url]")
    assert html == "<p>[url]   [/url]</p>"


def test_url_bbcode_with_invalid_url(parse_to_html):
    html = parse_to_html("[url]invalid[/url]")
    assert html == (
        "<p>"
        "<a "
        'href="invalid" '
        'rel="external nofollow noopener" '
        'target="_blank" '
        'misago-rich-text="autolink"'
        ">"
        "invalid"
        "</a>"
        "</p>"
    )


def test_url_bbcode_with_escaped_content(parse_to_html):
    html = parse_to_html("[url]example\\.com[/url]")
    assert html == (
        "<p>"
        "<a "
        'href="example.com" '
        'rel="external nofollow noopener" '
        'target="_blank" '
        'misago-rich-text="autolink"'
        ">"
        "example.com"
        "</a>"
        "</p>"
    )


def test_url_bbcode_with_arg(parse_to_html):
    html = parse_to_html("[url=example.com]Hello[/url]")
    assert html == (
        "<p>"
        "<a "
        'href="example.com" '
        'rel="external nofollow noopener" '
        'target="_blank"'
        ">"
        "Hello"
        "</a>"
        "</p>"
    )


def test_url_bbcode_with_empty_arg(parse_to_html):
    html = parse_to_html("[url=]Hello[/url]")
    assert html == "<p>[url=]Hello[/url]</p>"


def test_url_bbcode_with_blank_arg(parse_to_html):
    html = parse_to_html("[url=   ]Hello[/url]")
    assert html == "<p>[url=   ]Hello[/url]</p>"


def test_url_bbcode_with_quoted_arg(parse_to_html):
    html = parse_to_html('[url="example.com"]Hello[/url]')
    assert html == (
        "<p>"
        '<a href="example.com" rel="external nofollow noopener" target="_blank">'
        "Hello"
        "</a>"
        "</p>"
    )


def test_url_bbcode_with_escaped_arg(parse_to_html):
    html = parse_to_html('[url="example\\.com"]Hello[/url]')
    assert html == (
        "<p>"
        '<a href="example.com" rel="external nofollow noopener" target="_blank">'
        "Hello"
        "</a>"
        "</p>"
    )


def test_url_bbcode_with_invalid_arg(parse_to_html):
    html = parse_to_html("[url=invalid]Hello[/url]")
    assert html == (
        "<p>"
        '<a href="invalid" rel="external nofollow noopener" target="_blank">'
        "Hello"
        "</a>"
        "</p>"
    )


def test_url_bbcode_with_arg_parses_content(parse_to_html):
    html = parse_to_html("[url=example.com]Hello **world**[/url]")
    assert html == (
        "<p>"
        '<a href="example.com" rel="external nofollow noopener" target="_blank">'
        "Hello <strong>world</strong>"
        "</a>"
        "</p>"
    )


def test_url_bbcode_with_escaped_closing_tag(parse_to_html):
    html = parse_to_html("[url=example.com]Hello\\[/url]")
    assert html == (
        "<p>"
        "["
        "<a "
        'href="http://url=example.com" '
        'rel="external nofollow noopener" '
        'target="_blank" '
        'misago-rich-text="autolink"'
        ">"
        "url=example.com</a>]Hello[/url]"
        "</p>"
    )
