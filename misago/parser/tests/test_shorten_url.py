from ..shortenurl import shorten_url


def test_shorten_url_strips_protocol():
    result = shorten_url("https://misago-project.org")
    assert result == "misago-project.org"


def test_shorten_url_strips_trailing_slash():
    result = shorten_url("https://misago-project.org/")
    assert result == "misago-project.org"


def test_shorten_url_keeps_trailing_slash_its_part_of_path():
    result = shorten_url("https://misago-project.org/lorem/")
    assert result == "misago-project.org/lorem/"


def test_shorten_url_strips_index_html():
    result = shorten_url("https://misago-project.org/index.html")
    assert result == "misago-project.org"


def test_shorten_url_strips_index_htm():
    result = shorten_url("https://misago-project.org/index.htm")
    assert result == "misago-project.org"


def test_shorten_url_strips_index_php():
    result = shorten_url("https://misago-project.org/index.php")
    assert result == "misago-project.org"


def test_shorten_url_strips_index_before_querystring():
    result = shorten_url("https://misago-project.org/index.html?hello")
    assert result == "misago-project.org/?hello"


def test_shorten_url_shortens_long_url():
    result = shorten_url(
        "https://en.wikipedia.org"
        "/wiki/Principles_of_user_interface_design_in_common_consumer_electronics"
    )
    assert result == (
        "en.wikipedia.org/wiki/Principles_of...ce_design_in_common_consumer_electronics"
    )


def test_shorten_url_works_with_short_relative_urls():
    result = shorten_url("/")
    assert result == "/"


def test_shorten_url_works_with_long_relative_urls():
    result = shorten_url("/thread/posts/lorem/ipsum/")
    assert result == "/thread/posts/lorem/ipsum/"


def test_linkified_text_is_shortened(parse_to_html):
    html = parse_to_html(
        "https://en.wikipedia.org"
        "/wiki/Principles_of_user_interface_design_in_common_consumer_electronics"
    )
    assert html == (
        "<p>"
        "<a "
        'href="https://en.wikipedia.org/wiki/Principles_of_user_interface_design_in_common_consumer_electronics" '
        'rel="external nofollow noopener" '
        'target="_blank" '
        'misago-rich-text="autolink"'
        ">"
        "en.wikipedia.org/wiki/Principles_of...ce_design_in_common_consumer_electronics"
        "</a>"
        "</p>"
    )


def test_autolink_text_is_shortened(parse_to_html):
    html = parse_to_html(
        "<https://en.wikipedia.org"
        "/wiki/Principles_of_user_interface_design_in_common_consumer_electronics>"
    )
    assert html == (
        "<p>"
        "<a "
        'href="https://en.wikipedia.org/wiki/Principles_of_user_interface_design_in_common_consumer_electronics" '
        'rel="external nofollow noopener" '
        'target="_blank" '
        'misago-rich-text="autolink"'
        ">"
        "en.wikipedia.org/wiki/Principles_of...ce_design_in_common_consumer_electronics"
        "</a>"
        "</p>"
    )
