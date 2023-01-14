from ..client import get_headers_dict


def test_empty_headers_dict_is_returned_for_none():
    headers = get_headers_dict(None)
    assert headers == {}


def test_empty_headers_dict_is_returned_for_empty_str():
    headers = get_headers_dict("")
    assert headers == {}


def test_empty_headers_dict_is_returned_for_empty_multiline_str():
    headers = get_headers_dict("  \n   \n  ")
    assert headers == {}


def test_header_is_returned_from_str():
    headers = get_headers_dict("Lorem: ipsum")
    assert headers == {"Lorem": "ipsum"}


def test_headers_str_content_is_cleaned():
    headers = get_headers_dict("  Lorem:   ips:um\n\n")
    assert headers == {"Lorem": "ips:um"}


def test_multiple_headers_are_returned_from_multiline_str():
    headers = get_headers_dict("Lorem: ipsum\nDolor: met")
    assert headers == {"Lorem": "ipsum", "Dolor": "met"}
