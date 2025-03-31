def test_mention(parse_to_html):
    html = parse_to_html("@John123")
    assert html == '<p><misago-mention username="John123"></p>'


def test_mention_is_passed_in_sentence(parse_to_html):
    html = parse_to_html("lorem @John123 ipsum")
    assert html == '<p>lorem <misago-mention username="John123"> ipsum</p>'


def test_mention_is_passed_in_parenthesis(parse_to_html):
    html = parse_to_html("(@John123)")
    assert html == '<p>(<misago-mention username="John123">)</p>'


def test_mention_is_not_parsed_in_link(parse_to_html):
    html = parse_to_html("[@John123](http://example.com)")
    assert (
        html
        == '<p><a href="http://example.com" rel="external nofollow noopener" target="_blank">@John123</a></p>'
    )


def test_mention_is_not_parsed_in_email(parse_to_html):
    html = parse_to_html("contact@example.com")
    assert html == (
        "<p>"
        '<a href="mailto:contact@example.com" rel="external nofollow noopener" target="_blank">contact@example.com</a>'
        "</p>"
    )
