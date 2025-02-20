from ..urls import clean_url


def test_clean_url_supports_relative_urls():
    assert clean_url("/") == "/"


def test_clean_url_prepends_http_to_unknown_protocol_url():
    assert clean_url("://example.com") == "http://example.com"


def test_clean_url_prepends_http_to_url_without_protocol():
    assert clean_url("example.com") == "http://example.com"
