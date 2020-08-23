from unittest.mock import Mock

from ..request import get_absolute_url


def test_absolute_url_is_built_for_given_url():
    request = Mock(base_url="http://something.com/")
    url = get_absolute_url(request, "/test/")
    assert url == "http://something.com/test/"


def test_absolute_url_returns_base_url_if_no_url_is_given():
    request = Mock(base_url="http://something.com/")
    url = get_absolute_url(request)
    assert url == "http://something.com"
