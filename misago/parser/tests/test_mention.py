def test_mention_user(user, parse_to_html, snapshot):
    html = parse_to_html("@" + user.username)
    assert html == snapshot


def test_mention_user_with_underscore_in_name(other_user, parse_to_html, snapshot):
    html = parse_to_html("@" + other_user.username)
    assert html == snapshot


def test_mention_is_syntax_insensitive(other_user, parse_to_html, snapshot):
    html = parse_to_html("@" + other_user.username.lower())
    assert html == snapshot


def test_mention_user_in_sentence(user, parse_to_html, snapshot):
    html = parse_to_html(f"lorem @{user.username} ipsum")
    assert html == snapshot


def test_mention_user_in_parenthesis(user, parse_to_html, snapshot):
    html = parse_to_html(f"(@{user.username})")
    assert html == snapshot


def test_mention_for_not_found_user(db, parse_to_html, snapshot):
    html = parse_to_html("this @User doesn't exist")
    assert html == snapshot


def test_mention_for_inactive_user(inactive_user, parse_to_html, snapshot):
    html = parse_to_html(f"this @{inactive_user.username} is inactive")
    assert html == snapshot


def test_mention_is_not_parsed_in_link(parse_to_html):
    html = parse_to_html("[@John123](http://example.com)")
    assert html == (
        "<p>"
        '<a href="http://example.com" rel="external nofollow noopener" target="_blank">'
        "@John123"
        "</a>"
        "</p>"
    )


def test_mention_is_not_parsed_in_bbcode_url(parse_to_html):
    html = parse_to_html("[url=http://example.com]@John123[/url]")
    assert html == (
        "<p>"
        '<a href="http://example.com" rel="external nofollow noopener" target="_blank">'
        "@John123"
        "</a>"
        "</p>"
    )


def test_mention_is_not_parsed_in_email(parse_to_html):
    html = parse_to_html("contact@example.com")
    assert html == (
        "<p>"
        '<a href="mailto:contact@example.com" rel="external nofollow noopener" target="_blank">'
        "contact@example.com"
        "</a>"
        "</p>"
    )
