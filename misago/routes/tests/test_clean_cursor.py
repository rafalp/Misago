from unittest.mock import Mock

import pytest

from ..exceptions import HTTPNotFound
from ..utils import clean_cursor_or_404


def test_clean_cursor_is_returned_from_request():
    request = Mock(query_params={"cursor": "123"})
    cursor = clean_cursor_or_404(request)
    assert cursor == 123


def test_clean_cursor_is_none_if_not_set():
    request = Mock(query_params={})
    cursor = clean_cursor_or_404(request)
    assert cursor is None


def test_clean_cursor_number_raises_not_found_exception_for_invalid_cursor():
    with pytest.raises(HTTPNotFound):
        request = Mock(query_params={"cursor": "invalid"})
        clean_cursor_or_404(request)


def test_clean_cursor_number_raises_not_found_exception_for_cursor_less_than_1():
    with pytest.raises(HTTPNotFound):
        request = Mock(query_params={"cursor": "0"})
        clean_cursor_or_404(request)

    with pytest.raises(HTTPNotFound):
        request = Mock(query_params={"cursor": -1})
        clean_cursor_or_404(request)
