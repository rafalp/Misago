from unittest.mock import Mock

import pytest

from ..exceptions import HTTPNotFound
from ..utils import ExplicitFirstPage, clean_page_number_or_404


def test_clean_page_number_is_returned_from_request():
    request = Mock(path_params={"page": "123"})
    page_number = clean_page_number_or_404(request)
    assert page_number == 123


def test_clean_page_number_is_none_if_not_set():
    request = Mock(path_params={})
    page_number = clean_page_number_or_404(request)
    assert page_number is None


def test_clean_page_number_raises_not_found_exception_for_invalid_page():
    with pytest.raises(HTTPNotFound):
        request = Mock(path_params={"page": "invalid"})
        clean_page_number_or_404(request)


def test_clean_page_number_raises_explicit_first_page_exception_for_page_1():
    with pytest.raises(ExplicitFirstPage):
        request = Mock(path_params={"page": "1"})
        clean_page_number_or_404(request)


def test_clean_page_number_raises_not_found_exception_for_page_less_than_1():
    with pytest.raises(HTTPNotFound):
        request = Mock(path_params={"page": "0"})
        clean_page_number_or_404(request)

    with pytest.raises(HTTPNotFound):
        request = Mock(path_params={"page": -1})
        clean_page_number_or_404(request)
