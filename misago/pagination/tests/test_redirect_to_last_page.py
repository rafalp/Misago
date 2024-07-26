from unittest.mock import Mock

from ..cursor import EmptyPageError
from ..redirect import redirect_to_last_page


def test_redirect_to_last_page_builds_redirect_without_cursor_for_first_page():
    request = Mock(
        path_info="/path-info/",
        GET=Mock(dict=Mock(return_value={"cursor": 100})),
    )
    redirect = redirect_to_last_page(request, EmptyPageError(None))

    assert redirect.status_code == 302
    assert redirect["location"] == "/path-info/"


def test_redirect_to_last_page_builds_redirect_with_cursor_for_first_page():
    request = Mock(
        path_info="/path-info/",
        GET=Mock(dict=Mock(return_value={"cursor": 100})),
    )
    redirect = redirect_to_last_page(request, EmptyPageError(40))

    assert redirect.status_code == 302
    assert redirect["location"] == "/path-info/?cursor=40"


def test_redirect_to_last_page_with_cursor_keeps_other_querystring_items():
    request = Mock(
        path_info="/path-info/",
        GET=Mock(dict=Mock(return_value={"cursor": 100, "search": "query"})),
    )
    redirect = redirect_to_last_page(request, EmptyPageError(40))

    assert redirect.status_code == 302
    assert redirect["location"] == "/path-info/?cursor=40&search=query"


def test_redirect_to_last_page_without_cursor_keeps_other_querystring_items():
    request = Mock(
        path_info="/path-info/",
        GET=Mock(dict=Mock(return_value={"cursor": 100, "search": "query"})),
    )
    redirect = redirect_to_last_page(request, EmptyPageError(None))

    assert redirect.status_code == 302
    assert redirect["location"] == "/path-info/?search=query"
