from ..parser import parse


def test_bold_bbcode(request_mock, user, snapshot):
    text = "Lorem [b]ipsum[/b]!"
    result = parse(text, request_mock, user, minify=False)
    snapshot.assert_match(result["parsed_text"])


def test_italics_bbcode(request_mock, user, snapshot):
    text = "Lorem [i]ipsum[/i]!"
    result = parse(text, request_mock, user, minify=False)
    snapshot.assert_match(result["parsed_text"])


def test_underline_bbcode(request_mock, user, snapshot):
    text = "Lorem [u]ipsum[/u]!"
    result = parse(text, request_mock, user, minify=False)
    snapshot.assert_match(result["parsed_text"])


def test_inline_bbcode_can_be_mixed_with_markdown(request_mock, user, snapshot):
    text = "Lorem [b]**ipsum**[/b]!"
    result = parse(text, request_mock, user, minify=False)
    snapshot.assert_match(result["parsed_text"])


def test_image_bbcode(request_mock, user, snapshot):
    text = "Lorem [img]https://placekitten.com/g/1200/500[/img] ipsum"
    result = parse(text, request_mock, user, minify=False)
    snapshot.assert_match(result["parsed_text"])


def test_image_bbcode_is_case_insensitive(request_mock, user, snapshot):
    text = "Lorem [iMg]https://placekitten.com/g/1200/500[/ImG] ipsum"
    result = parse(text, request_mock, user, minify=False)
    snapshot.assert_match(result["parsed_text"])


def test_url_bbcode(request_mock, user, snapshot):
    text = "Lorem [url]https://placekitten.com/g/1200/500[/url] ipsum"
    result = parse(text, request_mock, user, minify=False)
    snapshot.assert_match(result["parsed_text"])


def test_url_bbcode_includes_nofollow_and_noopener(request_mock, user, snapshot):
    text = "Lorem [url]https://placekitten.com/g/1200/500[/url] ipsum"
    result = parse(text, request_mock, user, minify=False)
    assert 'rel="nofollow noopener"' in result["parsed_text"]


def test_url_bbcode_with_link_text(request_mock, user, snapshot):
    text = "Lorem [url=https://placekitten.com/g/1200/500]dolor[/url] ipsum"
    result = parse(text, request_mock, user, minify=False)
    snapshot.assert_match(result["parsed_text"])


def test_url_bbcode_with_long_link_text(request_mock, user, snapshot):
    text = "Lorem [url=https://placekitten.com/g/1200/500]dolor met[/url] ipsum"
    result = parse(text, request_mock, user, minify=False)
    snapshot.assert_match(result["parsed_text"])


def test_url_bbcode_with_quotes_and_link_text(request_mock, user, snapshot):
    text = 'Lorem [url="https://placekitten.com/g/1200/500"]dolor[/url] ipsum'
    result = parse(text, request_mock, user, minify=False)
    snapshot.assert_match(result["parsed_text"])


def test_url_bbcode_with_quotes_and_long_link_text(request_mock, user, snapshot):
    text = 'Lorem [url="https://placekitten.com/g/1200/500"]dolor met[/url] ipsum'
    result = parse(text, request_mock, user, minify=False)
    snapshot.assert_match(result["parsed_text"])
