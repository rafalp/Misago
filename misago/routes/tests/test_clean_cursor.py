from unittest.mock import Mock

import pytest

from ..exceptions import HTTPNotFound
from ..utils import clean_cursor_or_404


def test_clean_after_cursor_is_returned_from_request():
    request = Mock(query_params={"after": "123"})
    after, before = clean_cursor_or_404(request)
    assert after == 123
    assert before is None


def test_clean_before_cursor_is_returned_from_request():
    request = Mock(query_params={"before": "321"})
    after, before = clean_cursor_or_404(request)
    assert before == 321
    assert after is None


def test_clean_cursor_is_none_if_not_set():
    request = Mock(query_params={})
    after, before = clean_cursor_or_404(request)
    assert after is None
    assert before is None


def test_clean_cursor_number_raises_not_found_exception_for_invalid_after_cursor():
    with pytest.raises(HTTPNotFound):
        request = Mock(query_params={"after": "invalid"})
        clean_cursor_or_404(request)


def test_clean_cursor_number_raises_not_found_exception_for_invalid_before_cursor():
    with pytest.raises(HTTPNotFound):
        request = Mock(query_params={"before": "invalid"})
        clean_cursor_or_404(request)


def test_clean_cursor_number_raises_not_found_exception_for_two_cursors():
    with pytest.raises(HTTPNotFound):
        request = Mock(query_params={"after": "1", "before": 2})
        clean_cursor_or_404(request)


def test_clean_cursor_number_raises_not_found_exception_for_cursor_less_than_1():
    with pytest.raises(HTTPNotFound):
        request = Mock(query_params={"after": "0"})
        clean_cursor_or_404(request)

    with pytest.raises(HTTPNotFound):
        request = Mock(query_params={"after": -1})
        clean_cursor_or_404(request)

    with pytest.raises(HTTPNotFound):
        request = Mock(query_params={"before": "0"})
        clean_cursor_or_404(request)

    with pytest.raises(HTTPNotFound):
        request = Mock(query_params={"before": -1})
        clean_cursor_or_404(request)
